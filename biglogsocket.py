#!/usr/bin/env python3

from ast import Num
import asyncio
from fastapi import WebSocket
from mavsdk import System
from mavsdk import telemetry
# import sys

# 大无人机日志的websocket实现
class biglogsocket:
    uavport = ""
    battery = []
    location = []

    # 套接字
    websocket : WebSocket

    async def run(self):

        drone = System()
        await drone.connect(system_address="tcp://" + self.uavport)

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

        # 套接字accept
        await self.websocket.accept()
        while True:

            # --------------------电池电压和电量百分数
            async for terrain_info2 in drone.telemetry.battery():
                self.battery = terrain_info2
                break
            # --------------------position()当前位置（更新当前位置）
            async for terrain_info5 in drone.telemetry.position():
                self.location = terrain_info5
                break

            # 套接字发送data
            # await self.websocket.send_json()
            await self.websocket.send_text({"battery":self.battery,"location":self.location})

            # # 可以-----
            # data = "12345"
            # await self.websocket.send_text(f"Message text was: 1234sitllogsocket.py")
            # # --------
