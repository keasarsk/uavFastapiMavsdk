#!/usr/bin/env python3

import asyncio
from time import sleep
from mavsdk import System
import sys

class terminationreturn():
    async def run(self):
        drone = System()
        await drone.connect(system_address="udp://:" + sys.argv[1])

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered!")
                break

        print("-- pause mission")
        await drone.mission.pause_mission()

        print("-- clear mission")
        await drone.mission.clear_mission()

        await sleep(1000)

        print("-- Return To Launch")
        await drone.action.return_to_launch()
