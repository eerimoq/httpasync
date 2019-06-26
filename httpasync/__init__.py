import logging
import asyncio
import httptools

from .version import __version__


LOGGER = logging.getLogger(__name__)



class Protocol:

    def on_message_begin(self):
        print('on_message_begin')

    def on_url(self, url):
        print(f'on_url: {url}')

    def on_header(self, name, value):
        print(f'on_header: {name}: {value}')

    def on_headers_complete(self):
        print('on_headers_complete')

    def on_body(self, body):
        print(f'on_body: {body}')

    def on_message_complete(self):
        print('on_message_complete')

    def on_chunk_header(self):
        print('on_chunk_header')

    def on_chunk_complete(self):
        print('on_chunk_header')

    def on_status(self, status):
        print(f'on_status: {status}')


parser = httptools.HttpRequestParser(Protocol())
data = ('GET / HTTP/1.1\r\n'
        'Host: www.example.com\r\n'
        'User-Agent: curl/7.47.0\r\n'
        'Accept: */*\r\n'
        '\r\n').encode('ascii')

parser.feed_data(data[:2])
parser.feed_data(data[2:])
print(parser.get_http_version())
print(parser.get_method())


class Server:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._routes = {}

    def add_route(self, path, handler):
        self._routes[path] = handler

    async def serve_forever(self):
        """Setup a listener socket and forever serve clients. This coroutine
        only ends if cancelled by the user.

        """

        listener = await asyncio.start_server(self.serve_client,
                                              self._host,
                                              self._port)

        LOGGER.info('Listening for clients on %s.',
                    listener.sockets[0].getsockname())

        async with listener:
            await listener.serve_forever()

    async def serve_client(self, reader, writer):
        print('Client connected. Closing...')
        writer.close()
