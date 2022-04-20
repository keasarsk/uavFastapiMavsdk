#!/usr/bin/env python3

from ast import Num
import asyncio
from mavsdk import System
# from mavsdk import telemetry
# import sys

# from main import location

class Location_log:
    uavport = ""
    battery = []
    location = []

    async def run(self):

        drone = System()
        # await drone.connect(system_address="udp://:" + uav_port)
        # await drone.connect(system_address="udp://:1454" + self.num)
        await drone.connect(system_address="tcp://"+ self.uavport)


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

        # 电池电压和电量百分数
        # Battery: [id: 0, voltage_v: 15.100000381469727, remaining_percent: 0.5099999904632568]
        async for terrain_info2 in drone.telemetry.battery():
            print(terrain_info2)
            print("-----------self.battery-------------")
            self.battery = terrain_info2
            print(self.battery)
            break

        # ---------------------position()当前位置（更新当前位置）
        # Position: [latitude_deg: 47.3977693, longitude_deg: 8.545593499999999, absolute_altitude_m: 488.0790100097656, relative_altitude_m: 0.009000000543892384]
        print(" drone.telemetry.position()")
        async for terrain_info5 in drone.telemetry.position():
            print("----------------------drone.telemetry.position---------------")
            print(terrain_info5)
            self.location = terrain_info5
            print("----------self.location------------")
            print(self.location)
            print("----------------------")
            break

        # # ----------------------home()更新home为当前位置
        # print(" drone.telemetry.home()")
        # async for terrain_info7 in drone.telemetry.home():
        #     print(terrain_info7)
        #     break

    # async def get(self):
    #     return self.location

    async def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
        # loop.run_forever(self.run())
        # loop.close()
        # print(a)
        
# if __name__ == '__main__':
#     a = Location_log()
#     a.start()
    # a.run()
    # a.test()
    # a.run()