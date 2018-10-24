import asyncio
import logging
import json
from uuid import UUID

import aioredis
from aiocassandra import aiosession
from cassandra.cluster import Cluster
from cassandra import util

import config_logging

log = logging.getLogger(__name__)


LAST_ID_KEY = "devices.stream-last-ids"
STREAM = "devices.stream"


async def main(session):
    aiosession(session)

    redis = await aioredis.create_redis("redis://localhost")

    last_id = await redis.get(LAST_ID_KEY)

    if last_id:
        log.info(f"Starting consuming messages from {last_id}")
        last_id = [last_id]

    streams = redis.streams.consumer([STREAM], latest_ids=last_id, encoding="utf-8")

    async for message in streams:
        # message is a tuple (stream, id, order_dict)
        log.info(f"Got message from device {message[2]['device']}")

        last_id = streams.last_ids_for_stream[STREAM]
        log.info(f"Set last id to: {last_id}")
        await redis.set(LAST_ID_KEY, last_id)

        data = dict(**message[2])
        deviceid = data.pop("device")
        timestamp = util.datetime_from_timestamp(float(data.pop("timestamp")))

        query = session.prepare(
            """
            INSERT INTO devices ("deviceid", "timestamp", "data") VALUES (?, ?, ?)
            """
        )

        await session.execute_future(
            query, (UUID(deviceid), timestamp, json.dumps(data))
        )

        await asyncio.sleep(2)


if __name__ == "__main__":
    config_logging.setup()

    cluster = Cluster(compression=True)
    session = cluster.connect("devices")

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(session))
    finally:
        cluster.shutdown()
        loop.close()
