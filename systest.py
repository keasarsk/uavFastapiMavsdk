#!/usr/bin/env python3

import asyncio
import sys
# from ./main import

async def run():
    print("sys.argv:",sys.argv)
    # print(type(sys.argv))
    # print(sys.argv[1])
    # a = ''.join(sys.argv[1])
    # print(a)
    # print(type(a))
    # print(''.join(sys.argv[1]))
    print("1234")


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
# loop.close()