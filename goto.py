#!/usr/bin/env python3

import asyncio
from mavsdk import System
import sys
class goto():
    async def run():
        drone = System()
        await drone.connect(system_address="udp://:" + sys.argv[1])

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print("Drone discovered!")
                break

        print("Waiting for drone to have a global position estimate...")
        async for health in drone.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break


        # print("Fetching amsl altitude at home location....")
        # print("drone.telemetry.home():", type(drone.telemetry.home()))
        # # print("drone.telemetry.home():",drone.telemetry.home())
        #
        async for terrain_info in drone.telemetry.home():
            print(terrain_info)
            absolute_altitude = terrain_info.absolute_altitude_m
            break


        print("-- Arming")
        await drone.action.arm()

        print("-- arm-position")
        async for terrain_info2 in drone.telemetry.position():
            print(terrain_info2)
            break

        print("-- Taking off")
        await drone.action.takeoff()

        await asyncio.sleep(1)
        # To fly drone 1m above the ground plane
        flying_alt = absolute_altitude + 1.0
        # goto_location() takes Absolute MSL altitude
        # await drone.action.goto_location(47.397606, 8.543060, flying_alt, 0)
        await drone.action.goto_location(40, 116, 10, 0)

        # while True:
        #     print("Staying connected, press Ctrl-C to exit")
        #
        #     await asyncio.sleep(3)
        await asyncio.sleep(1500)
        print("-- goto-position")
        async for terrain_info2 in drone.telemetry.position():
            print(terrain_info2)
            break


# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())
