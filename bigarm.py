#!/usr/bin/env python3

import asyncio
from mavsdk import System

class big():
    async def run(self):
        print("rtyui")
        drone = System()
        print("rtyui")
        if (await drone.connect(system_address="tcp://192.168.1.81:8080")):
            print("uav0---false!")
        else:
            print("uav0---ready!")

        drone1 = System()
        if (await drone1.connect(system_address="tcp://192.168.1.191:8080")):
            print("uav1---false!")
        else:
            print("uav1---ready!")


# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())