import logging
import asyncio

from .version import __version__


LOGGER = logging.getLogger(__name__)


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
