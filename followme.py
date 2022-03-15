#!/usr/bin/env python3

#This example shows how to use the follow me plugin
#跟随目标

import asyncio
from mavsdk import System
from mavsdk.follow_me import (Config, FollowMeError, TargetLocation)
import sys
default_height = 8.0 #in Meters
follow_distance = 2.0 #in Meters, this is the distance that the drone will remain away from Target while following it
# (这是无人机在跟踪目标时保持的距离)
#Direction relative to the Target
#Options are NONE, FRONT, FRONT_LEFT, FRONT_RIGHT, BEHIND
direction = Config.FollowDirection.BEHIND
responsiveness = 0.02# responsiveness 响应

#This list contains fake location coordinates (These coordinates are obtained from mission.py example)
#这个列表包含假设的位置坐标(这些坐标是从mission.py示例中获得的)
fake_location = [[47.398039859999997,8.5455725400000002],[47.398036222362471,8.5450146439425509],
                 [47.397825620791885,8.5450092830163271]]

async def fly_drone():
    drone = System()
    await drone.connect(system_address="udp://:" + sys.argv[1])

    #This waits till a mavlink based drone is connected
    #这要等到mavlink的无人机被连接
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    #Checking if Global Position Estimate is ok
    #检查全球位置估计是否正确
    async for global_lock in drone.telemetry.health():
        if global_lock.is_global_position_ok and global_lock.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    #Arming the drone
    #装备无人机
    print ("-- Arming")
    await drone.action.arm()

    async for terrain_info5 in drone.telemetry.position():
        print(terrain_info5)
        break
    #Follow me Mode requires some configuration to be done before starting the mode
    #drone启动前的一些配置
    conf = Config(default_height, follow_distance, direction, responsiveness)
    await drone.follow_me.set_config(conf)

    print ("-- Taking Off")
    await drone.action.takeoff()
    await asyncio.sleep(8)
    print ("-- Starting Follow Me Mode")
    await drone.follow_me.start()
    await asyncio.sleep(8)

    #This for loop provides fake coordinates from the fake_location list for the follow me mode to work
    #这个for循环提供假位置列表中的假坐标，以便follow me模式工作
    #In a simulator it won't make much sense though
    #但在模拟器中这并没有多大意义
    for latitude,longitude in fake_location:
        target = TargetLocation(latitude, longitude, 0, 0, 0, 0)
        print ("-- Following Target")
        await drone.follow_me.set_target_location(target)
        await asyncio.sleep(8)
        # async for terrain_info5 in drone.telemetry.position():
        #     print(terrain_info5)
        #     break


    #Stopping the follow me mode
    print ("-- Stopping Follow Me Mode")
    await drone.follow_me.stop()

    await asyncio.sleep(8)

    print("-- Return To Launch")
    await drone.action.return_to_launch()
    
    await asyncio.sleep(8)
    print ("-- Landing")
    await drone.action.land()

    await asyncio.sleep(8)
    async for terrain_info5 in drone.telemetry.position():
        print(terrain_info5)
        break


loop = asyncio.get_event_loop()
loop.run_until_complete(fly_drone())
