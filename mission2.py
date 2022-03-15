#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)
import os
import sys
async def run():
    drone = System()
    await drone.connect(system_address="udp://:" + sys.argv[1])

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered!")
            break

    # task
    print_mission_progress_task = asyncio.ensure_future(print_mission_progress(drone))
    print("print_mission_progress_task:")
    # print(type(print_mission_progress_task))
    print("    ", print_mission_progress_task)

    # list[task]
    running_tasks = [print_mission_progress_task]
    print("running_tasks:")
    # print(type(running_tasks))
    print("    ", running_tasks)

    # task
    termination_task = asyncio.ensure_future(
        observe_is_in_air(drone, running_tasks))
    print("termination_task:")
    # print(type(termination_task))
    print("    ", termination_task)

    with open(r'mission_items.txt', 'r') as mission_items_file_to_read:  # 打开文件，将其值赋予file_to_read
        txt_list = mission_items_file_to_read.readlines()  # 整行读取数据
        # while True:
        #     lines = mission_items_file_to_read.readlines()  # 整行读取数据
            # if not lines:  # 若该行为空
            #     break
            # else:
            #
            #     print("lines:",lines)
            #     print("type(lines):",type(lines))
            #     items.append(list(lines))
            #     print("items:", items)
            #     print("type(items):", type(items))
            #     # this_lines = lines.split('],[')  # 根据空格对字符串进行切割，由于切割后的数据类型有所改变(str-array)建议新建变量进行存储
            #     # items = this_lines
            #     # for this_line in this_lines:  # 遍历数组并输出
            #     #
            #     #     print(this_line)  # 直接在这里写处理代码就可以了，因为切割后的数组是按照顺序排列的，并且自动剔除了换行符
            #     #     # 但仍需注意，调试后发现切割后进行遍历的this_line变量为str格式，可能需要强制类型转换才能作为数字进行计算，所以这段代码同样支持英语汉语的分割输出
            #     # i+1
            #     print("～～～～～～～～～{}行啦啦啦～～～～～～～～～".format(i))
    print("\nRead mission_items.txt Finshed!")

    items_all = []
    for i in txt_list:
        items_all .append(i[1:-2])
    print("items_all:", items_all)

    items_latitude_deg = items_all[0].split(',')
    items_latitude_deg = list(map(float, items_latitude_deg))

    items_longitude_deg = items_all[1].split(',')
    items_longitude_deg = list(map(float, items_longitude_deg))

    items_relative_altitude_m = items_all[2].split(',')
    items_relative_altitude_m = list(map(float, items_relative_altitude_m))

    # items_speed_m_s = items_all[3].split(',')
    # items_speed_m_s = list(map(float, items_speed_m_s))

    # items_camera_action = items_all[4].split(',')
    # items_camera_action = list(map(float, items_camera_action))

    if items_all[5]:
        items_camera_photo_interval_s = items_all[5].split(',')
        items_camera_photo_interval_s = list(map(float, items_camera_photo_interval_s))
    if items_all[6]:
        items_yaw_deg = items_all[6].split(',')
        items_yaw_deg = list(map(float, items_yaw_deg))

    # print("items_latitude_deg:  ",items_latitude_deg)
    # print("items_longitude_deg:  ",items_longitude_deg)
    # print("items_relative_altitude_m:  ",items_relative_altitude_m)
    # print("items_speed_m_s:  ",items_speed_m_s)
    # print("type(items_speed_m_s):  ", type(items_speed_m_s))
    # print("items_speed_m_s[0],items_speed_m_s[1],items_speed_m_s[2]:  ",\
    #       items_speed_m_s[0],items_speed_m_s[1],items_speed_m_s[2])
    print(2222222)
    # print("len-items_latitude_deg:  ", len(items_latitude_deg))
    # print("len-items_longitude_deg:  ", len(items_longitude_deg))
    # print("len-items_relative_altitude_m:  ", len(items_relative_altitude_m))
    mission_items = []
    i = 0
    while i < len(items_latitude_deg):
        mission_items.append(MissionItem(items_latitude_deg[i],
                                         items_longitude_deg[i],
                                         5.0,
                                         10.0,
                                         True,
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.CameraAction.NONE,
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan')))
        i = i+1

    print("len(mission_items):",len(mission_items))
    # mission_items.append(MissionItem(sys.argv[2],
    #                                  sys.argv[3],
    #                                  sys.argv[4],
    #                                  sys.argv[5],
    #                                  True,
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  sys.argv[6],
    #                                  float('nan'),
    #                                  sys.argv[7],
    #                                  sys.argv[8],
    #                                  float('nan'),
    #                                  sys.argv[9]))

    # mission_items.append(MissionItem(47.395039859999997,
    #                                  8.5455725400000002,
    #                                  25,
    #                                  10,
    #                                  True,
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  MissionItem.CameraAction.NONE,
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  float('nan')))
    # mission_items.append(MissionItem(47.398036222362471,
    #                                  8.5450146439425509,
    #                                  25,
    #                                  10,
    #                                  True,
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  MissionItem.CameraAction.NONE,
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  float('nan')))
    # mission_items.append(MissionItem(47.399025620791885,
    #                                  8.550092830163271,
    #                                  25,
    #                                  10,
    #                                  True,
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  MissionItem.CameraAction.NONE,
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  float('nan'),
    #                                  float('nan')))

    mission_plan = MissionPlan(mission_items)

    await drone.mission.set_return_to_launch_after_mission(True)

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting mission")
    await drone.mission.start_mission()

    # await asyncio.sleep(10)
    await termination_task




async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")

async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return


loop = asyncio.get_event_loop()
loop.run_until_complete(run())


# loop.close()