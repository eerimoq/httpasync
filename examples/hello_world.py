import asyncio
import httpasync


class Index:

    def get(self, request, response):
        response.text = 'Hello world!'


async def main():
    server = httpasync.Server('localhost', 8080)
    server.add_route('/', Index())

    await server.serve_forever()


asyncio.run(main())
