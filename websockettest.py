#!/usr/bin/env python3


from time import sleep
from tokenize import Pointfloat
from fastapi import WebSocket

# import sys

# 大无人机日志的websocket实现
class websocket:
    
    # 套接字
    websocket : WebSocket

    async def run(self):
        # voltage_v: 0
        # remaining_percent: 0
        # latitude_deg: 0
        # longitude_deg: 8
        # absolute_altitude_m: 4
        # relative_altitude_m: 0
        # 套接字accept
        await self.websocket.accept()
        while True:

            # # 可以-----
            # data = "12345"
            # dict = {"battery":"10%","lat":"39.0"}
            Battery = {"id": 0, "voltage_v": 15.100000381469727, "remaining_percent": 0.5099999904632568}

            # await self.websocket.send_text(f"Message text was: 1234sitllogsocket.py")
            Position = {"latitude_deg": 47.3977693, "longitude_deg": 8.545593499999999, "absolute_altitude_m": 488.0790100097656, "relative_altitude_m": 0.009000000543892384}
        
            # await self.websocket.send_json(dict,Battery,Position)
            await self.websocket.send_json({"bat":Battery,"pos":Position})
            # await self.websocket.send_json(Position)
            # await sleep(1)

