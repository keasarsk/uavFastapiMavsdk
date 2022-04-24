#!/usr/bin/env python3

# import asyncio
from mavsdk import System

class bigtakeoff():
    async def run1(self):
        drone = System()
        await drone.connect(system_address="tcp://192.168.1.81:8080")

        # print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered!")
                break

        print("-- big81 Arming")
        await drone.action.arm()

        print("-- big81 1Taking off") 
        await drone.action.takeoff()

    
    async def run2(self):
        drone = System()
        await drone.connect(system_address="tcp://192.168.1.191:8080")

        # print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered!")
                break

        print("-- big191 Arming")
        await drone.action.arm()

        print("-- big191 1Taking off") 
        await drone.action.takeoff()
