import aiohttp
import asyncio
from uuid import uuid4
import random
import time

devices = [uuid4().hex for device in range(100)]


async def post(session, url, json):
    async with session.post(url, json=json) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            json = {
                "device": random.choice(devices),
                "timestamp": time.time(),
                "data": {
                    "sensor_1": 232,
                    "sensor_2": 2323,
                    "sensor_3": 503490
                }
            }
            asyncio.sleep(1)
            html = await post(session, 'http://python.org', json=json)
            print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
