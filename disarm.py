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


    print("-- Arming")
    await drone.action.arm()
    print("-- takeoff")
    await drone.action.takeoff()
    print("-- sleep")
    await asyncio.sleep(5)
    print("-- return_to_launch")
    await drone.action.return_to_launch()
    print("-- Arming")
    await drone.action.terminate()

    print("-- DisArming")
    await drone.action.disarm()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())