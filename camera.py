#!/usr/bin/env python3

'''
    相机模块
    输出相机模式
    输出摄像机状态
    设置摄像机模式
'''

import asyncio

from mavsdk.camera import (CameraError, Mode)
from mavsdk import System
import sys

async def print_mode(drone):
    async for mode in drone.camera.mode():
                    # camera.mode() Subscribe to camera mode updates.
        print(f"Camera mode: {mode}")


async def print_status(drone):
    async for status in drone.camera.status():
                    # camera.status() Subscribe to camera status updates.摄像头最新状态
        print(status)

# async def run():
#     drone = System()
#     await drone.connect(system_address="udp://:14540")
#
#     print("Waiting for drone to connect...")
#     async for state in drone.core.connection_state():
#         if state.is_connected:
#             print(f"Drone discovered!")
#             break
#


async def run():
    drone = System()
    await drone.connect(system_address="udp://:" + sys.argv[1])

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    print("arming")
    await drone.action.arm()
    await drone.action.takeoff()
    await drone.action.hold()

    # print("camera mode:")
    # await print_mode(drone)
    async for mode in drone.camera.mode():
        # camera.mode() Subscribe to camera mode updates.
        print(f"Camera mode: {mode}")
        break
    print("333")
    print(drone.camera.information())
    print(drone.telemetry.position())
    async for terrain_info5 in drone.camera.information():
        print(terrain_info5)
        break
    print("444")
    print(drone.camera.current_settings())
    async for info in drone.camera.current_settings():
        print(f"info: {info}")
        break

    print("111")
    # print("possible_setting_options:")
    # async for info in drone.camera.possible_setting_options():
    #     print(info)
    #     break
    print("information:")
    # async for info in drone.camera.information():
    #     print(info)
    #     break
    print(type(drone.camera.information()))
    print("222")


    print_mode_task = asyncio.ensure_future(print_mode(drone))
                    # asyncio.ensure_future(obj, *, loop=None)
                    # 如果 obj 不是Future、 Task 或 类似 Future 对象会引发一个 TypeError 异常
                            # .ensure_future() 接受任意 awaitable 对象
                            # awaitable 对象: 能在 await 表达式中使用的对象。可以是 coroutine 或是具有 __await__() 方法的对象
                            # 具有 __await__() 方法: 例如 Future、 Task 或 类似 Future 的对象
    print_status_task = asyncio.ensure_future(print_status(drone))


    print(type(print_status_task))
    print(print_status_task)
    # async for info in print_status_task:
    #     print(info)
    #     break
    #
    # async for info in print_mode_task:
    #     print(info)
    #     break



    running_tasks = [print_mode_task, print_status_task]

    print("Setting mode to 'PHOTO'")
    try:
        await drone.camera.set_mode(Mode.PHOTO)
                    # async set_mode(mode) Set camera mode.
    except CameraError as error:
        print(f"Setting mode failed with error code: {error._result.result}")

    await asyncio.sleep(2)

    print("Taking a photo")
    try:
        await drone.camera.take_photo()
    except CameraError as error:
        print(f"Couldn't take photo: {error._result.result}")

    # Shut down the running coroutines (here 'print_mode()' and
    # 'print_status()')
    for task in running_tasks:
        task.cancel()
            # task.cancel() 请求取消 Task 对象，清理时候用
        try:
            await task
        except asyncio.CancelledError:
            pass
    await asyncio.get_event_loop().shutdown_asyncgens()
                                    # 安排所有当前打开的 asynchronous generator 对象通过 aclose() 调用来关闭。
                                    # 在调用此方法后，如果有新的异步生成器被迭代事件循环将会发出警告。
                                    # 这应当被用来可靠地完成所有已加入计划任务的异步生成器。




loop = asyncio.get_event_loop()
loop.run_until_complete(run())
