import json
import os
import random

from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import asyncio


class EventBus:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.nc = NATS()
        self.sc = STAN()

    def run(self):
        self.loop.run_until_complete(self.__run(self.loop))

    async def __run(self, loop):
        try:
            await self.nc.connect(servers=[os.getenv('NATS_URL')], io_loop=loop)
            await self.sc.connect(os.getenv('NATS_CLUSTER_ID'),
                                  os.getenv('NATS_CLIENT_ID') + str(random.randint(1000, 9999)), nats=self.nc)
        except Exception as e:
            print(e)

    def byte_encode_data(self, normal_str):
        return json.dumps(normal_str).encode('utf-8')

    def byte_decode_data(self, byte_str):
        return json.loads((byte_str.decode('utf-8').replace("'", '"')))
