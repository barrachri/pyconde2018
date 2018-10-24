import asyncio
from uuid import uuid4
import random
import time
import logging

import aiohttp

import config_logging

log = logging.getLogger(__name__)

URI = "http://localhost:8888"

# devices id
DEVICES = [
    "7ab5e408-aacf-42ee-8190-fed08a73c3b7",
    "41d76057-3f51-4189-9212-79050283f797",
    "18d645bd-ea3e-4b0a-aa2c-bc7f0a1d39db",
    "cae1c6d0-89cf-4bfd-9bfd-755aa705ffbd",
    "7b725e97-1bb1-4083-8212-f6430209452b",
    "e6b3b467-1ebb-4b16-b8d1-6b9a1eefb8a7",
    "f56bbe84-2a3e-4bf0-9873-df8c91552151",
    "d71ef56f-4dcf-49b4-b7b8-939860c170b9",
    "52dca9bb-6e95-4934-93ba-15a6e621df0e",
    "2c707efb-756d-4bbd-a5ae-6f4da4b212b5",
]

# device orientation
orientations = ["top", "bottom", "left", "right"]


async def post(session, url, json):
    async with session.post(url, json=json) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        while True:

            data = {
                "device": random.choice(DEVICES),
                "timestamp": time.time(),
                "sensor_1": random.random(),
                "sensor_2": random.uniform(0, 5),
                "sensor_3": random.uniform(5, 10),
                "orientation": random.choice(orientations),
            }

            log.info(f"Generating new message for {URI} with {data}")

            await post(session, URI, json=data)

            # sleep for 2 secs
            await asyncio.sleep(2)


if __name__ == "__main__":
    config_logging.setup()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    finally:
        loop.close()
