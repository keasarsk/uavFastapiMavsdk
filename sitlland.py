#!/usr/bin/env python3

import asyncio
from mavsdk import System
import sys

class sitlland():
    uavport : str
    async def run(self):

        drone = System()
        await drone.connect(system_address="udp://:" + self.uavport)

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered!")
                break

        print("-- Landing")
        await drone.action.land()

        await asyncio.sleep(5)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())