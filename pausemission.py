#!/usr/bin/env python3

from mavsdk import System

class pausemission():
    uavport = ""
    async def run(self):
        drone = System()
        await drone.connect(system_address="tcp://"+ self.uavport)

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print("Drone discovered!")
                break

        print("pausemission----------")
        await drone.mission.pause_mission()