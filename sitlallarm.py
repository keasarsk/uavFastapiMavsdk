#!/usr/bin/env python3

import asyncio
from mavsdk import System

class sitlallarm():
    async def run(self):
        drone = System()
        if (await drone.connect(system_address="udp://:14540")):
            print("uav0---false!")
        else:
            print("uav0---ready!")

        drone1 = System()
        if (await drone1.connect(system_address="udp://:14541")):
            print("uav1---false!")
        else:
            print("uav1---ready!")

        drone2 = System()
        if (await drone2.connect(system_address="udp://:14542")):
            print("uav2---false!")
        else:
            print("uav2---ready!")

        drone3 = System()
        if (await drone3.connect(system_address="udp://:14543")):
            print("uav3---false!")
        else:
            print("uav3---ready!")


# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())