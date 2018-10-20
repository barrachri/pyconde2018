from aiohttp import web
from json import JSONDecodeError


async def handle(request):

    try:
        data = await request.json_response()
    except JSONDecodeError:
        return web.json_response({"status": "error"}, status=403)

    # send data to the stream

    return web.json_response(data)

app = web.Application()
app.add_routes([web.post('/', handle)])

web.run_app(app)
