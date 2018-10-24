import json
import logging

from aiohttp import web
import aioredis

import config_logging

log = logging.getLogger(__name__)

REDIS_STREAM = "devices.stream"


async def handle(request):

    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"status": "error"}, status=403)

    redis = request.app["redis"]

    log.info(f"Creating new message into stream {REDIS_STREAM} with {data}")
    await redis.xadd(REDIS_STREAM, data)

    return web.json_response({"status": "ok"})


async def start_redis_connection(app):
    log.info("Create Redis connection")
    app["redis"] = await aioredis.create_redis(("localhost", 6379), loop=app.loop)


async def stop_redis_connection(app):
    app["redis"].close()
    await app["redis"]


if __name__ == "__main__":
    config_logging.setup()

    app = web.Application()
    app.add_routes([web.post("/", handle)])

    app.on_startup.append(start_redis_connection)
    app.on_cleanup.append(stop_redis_connection)

    web.run_app(app, port=8888)
