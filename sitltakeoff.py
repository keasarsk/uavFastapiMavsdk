#!/usr/bin/env python3

import asyncio
from mavsdk import System
import sys

class sitltakeoff():
    uavport = str

    async def run(self):
        drone = System()
        await drone.connect(system_address="udp://:" + self.uavport)

        # print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered!")
                break

        # 必须写这里 因为后续飞行操作基本在takeoff后所以arm应该在这里
        # 假如不在，landing后就自动disarming，无法再takeoff
        print("-- Arming")
        await drone.action.arm()

        print("-- Taking off") 
        await drone.action.takeoff()
