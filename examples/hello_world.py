import asyncio
import httpasync


class Index:

    async def get(self, _request, response):
        response.text = 'Hello, world!'


class Hello:

    async def get(self, _request, response, name):
        response.text = f'Hello, {name}!'


class File:

    def __init__(self):
        self._data = b'Hello, world!'

    async def get(self, _request, response):
        response.data = self._data

    async def post(self, request, _response):
        field = await next(request.multipart)
        self._data = await field.read()


async def main():
    server = httpasync.Server('localhost', 8080)
    server.add_route('/', Index())
    server.add_route('/hello/{name}', Hello())
    server.add_route('/file', File())

    await server.serve_forever()


asyncio.run(main())
