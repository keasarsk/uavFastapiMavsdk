#!/usr/bin/env python3.6

# import asyncio
# from mavsdk import System


# async def run():
#     drone = System()

#     await drone.connect(system_address="tcp://192.168.1.81:8080")

#     async for state in drone.core.connection_state():
#         if state.is_connected:
#             print(f"Drone discovered!")
#             break

#     print("-- Arming")
#     await drone.action.arm()


# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())
# loop.close()

import asyncio
from mavsdk import System


async def run():

    print("Waiting...")

    drone = System()
    # await drone.connect(system_address="tcp://192.168.1.81:8080")
    await drone.connect(system_address="udp://127.0.0.1:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    # print("Waiting for drone to have a global position estimate...")
    # async for health in drone.telemetry.health():
    #     if health.is_global_position_ok:
    #         print("Global position estimate ok")
    #         break

    print("-- Arming")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
