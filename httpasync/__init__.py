import re
import logging
import asyncio
import httptools

from .version import __version__


LOGGER = logging.getLogger(__name__)


class Request:

    def __init__(self):
        pass


class Response:

    def __init__(self):
        self.status = 200
        self.data = b''

    @property
    def text(self):
        return self.data.decode('utf-8')

    @text.setter
    def text(self, text):
        self.data = text.encode('utf-8')


class Protocol:

    def __init__(self):
        self.url = None
        self.message_complete = False

    def on_url(self, url):
        self.url = url.decode('utf-8')

    def on_message_complete(self):
        self.message_complete = True


class Server:

    def __init__(self, host, port, routes):
        self._host = host
        self._port = port
        self._routes = []

        for route, handler in routes:
            pattern = re.sub(r'\{([^\}]+)\}', r'(?P<\1>[^/]+)', route)
            re_route = re.compile(f'^{pattern}$')
            self._routes.append((re_route, handler))

    async def serve_forever(self):
        """Setup a listener socket and forever serve clients. This coroutine
        only ends if cancelled by the user.

        """

        listener = await asyncio.start_server(self._serve_client,
                                              self._host,
                                              self._port)

        LOGGER.info('Listening for clients on %s.',
                    listener.sockets[0].getsockname())

        async with listener:
            await listener.serve_forever()

    def _unpack_url(self, url):
        for re_route, handler in self._routes:
            mo = re_route.match(url)

            if mo:
                return handler, mo.groups()

        return None, None

    async def _serve_client(self, reader, writer):
        """Serve a client.

        """

        protocol = Protocol()
        parser = httptools.HttpRequestParser(protocol)

        while not protocol.message_complete:
            parser.feed_data(await reader.readline())

        handler, params = self._unpack_url(protocol.url)
        response = Response()

        if handler is not None:
            method = parser.get_method()
            request = Request()

            if method == b'GET':
                await handler.get(request, response, *params)
            elif method == b'POST':
                await handler.post(request, response, *params)
            else:
                response.status = 405
        else:
            response.status = 404

        if response.status == 200:
            writer.write(('HTTP/1.0 200 OK\r\n'
                          f'Server: HTTPAsync/{__version__}\r\n'
                          'Date: Thu, 27 Jun 2019 05:56:10 GMT\r\n'
                          'Content-type: text/plain; charset=utf-8\r\n'
                          f'Content-Length: {len(response.data)}\r\n'
                          '\r\n').encode('utf-8') + response.data)

        writer.close()
