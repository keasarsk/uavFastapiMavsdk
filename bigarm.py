#!/usr/bin/env python3

import asyncio
from mavsdk import System

class big():
    uavport : str
    async def run(self):
        drone = System()
        if (await drone.connect(system_address="tcp://" + self.uavport)):
            print("uav1---false!")
        else:
            print("uav1---ready!")

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())