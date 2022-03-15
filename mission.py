#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)

import sys

async def run():
    drone = System()
    await drone.connect(system_address="udp://:"+sys.argv[1])

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered!")
            break

    # task
    print_mission_progress_task = asyncio.ensure_future(
        print_mission_progress(drone))
    print("print_mission_progress_task:")
    print(type(print_mission_progress_task))
    print(print_mission_progress_task)

    # list[task]
    running_tasks = [print_mission_progress_task]
    print("running_tasks:")
    print(type(running_tasks))
    print(running_tasks)

    # task
    termination_task = asyncio.ensure_future(
        observe_is_in_air(drone, running_tasks))
    print("termination_task:")
    print(type(termination_task))
    print(termination_task)



    mission_items = []
    mission_items.append(MissionItem(sys.argv[2],
                                     sys.argv[3],
                                     sys.argv[4],
                                     sys.argv[5],
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     sys.argv[6],
                                     float('nan'),
                                     sys.argv[7],
                                     sys.argv[8],
                                     float('nan'),
                                     sys.argv[9]))
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

    # print("-- takeoff")
    # await drone.action.takeoff()

    # await asyncio.sleep(8)

    print("-- Starting mission")
    await drone.mission.start_mission()

    # await asyncio.sleep(10)
    # print("termination_task:")
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