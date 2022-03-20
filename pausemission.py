#!/usr/bin/env python3

import asyncio
from mavsdk import System
import sys

async def run():

    drone = System()
    await drone.connect(system_address="udp://:" + sys.argv[1])

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break



    print("-- pause_mission")
    await drone.mission.pause_mission()

    # await asyncio.sleep(5)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())