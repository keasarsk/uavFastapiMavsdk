#!/usr/bin/env python3

import asyncio
from main import returntolaunch
from mavsdk import System
import sys

class returntolaunch():
    async def run():

        drone = System()
        await drone.connect(system_address="udp://:" + sys.argv[1])

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered!")
                break

        print("-- Return To Launch")
        await drone.action.return_to_launch()



# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())