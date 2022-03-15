#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk import telemetry
import sys
async def run():

    drone = System()
    await drone.connect(system_address="udp://:" + sys.argv[1])

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break

    print("arm")
    await drone.action.arm()

    async for terrain_info1 in drone.telemetry.gps_info():
        print(terrain_info1)
        break
    async for terrain_info2 in drone.telemetry.battery():
        print(terrain_info2)
        break

    # ---------------------position()当前位置（更新当前位置）
    print(" drone.telemetry.position()")
    async for terrain_info5 in drone.telemetry.position():
        print(terrain_info5)
        break
    print(" drone.telemetry.health()")
    async for terrain_info6 in drone.telemetry.health():
        print(terrain_info6)
        break
    # # ----------------------home()更新home为当前位置
    # print(" drone.telemetry.home()")
    # async for terrain_info7 in drone.telemetry.home():
    #     print(terrain_info7)
    #     break


loop = asyncio.get_event_loop()
loop.run_until_complete(run())