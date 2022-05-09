#!/usr/bin/env python3


from time import sleep
from fastapi import WebSocket

# import sys

# 大无人机日志的websocket实现
class websocket:
    
    # 套接字
    websocket : WebSocket

    async def run(self):
        # 套接字accept
        await self.websocket.accept()
        while True:

            # # 可以-----
            data = "12345"
            dict = {"battery":"10%","lat":"39.0"}
            # await self.websocket.send_text(f"Message text was: 1234sitllogsocket.py")
            await self.websocket.send_json(dict)
            # await sleep(1)
            # # --------
            # i=i+1
