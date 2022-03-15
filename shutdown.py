# 管用，需要drone在disarm之后 准备好关机的时候，不然报错

#!/usr/bin/env python3

import asyncio
import sys
from mavsdk import System


async def run():

    drone = System()
    await drone.connect(system_address="udp://:" + sys.argv[1])

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break



    print("-- ShutDown")
    await drone.action.shutdown()



loop = asyncio.get_event_loop()
loop.run_until_complete(run())