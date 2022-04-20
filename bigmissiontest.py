# 自带任务版本

import asyncio

from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)

class bigmissiontest():
    async def run(self):
        print("MissionTestWaiting...")

        drone = System()
        # await drone.connect(system_address="udp://:14540")
        await drone.connect(system_address="tcp://192.168.1.81:8080")

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print("Drone discovered!")
                break

        print_mission_progress_task = asyncio.ensure_future(
            print_mission_progress(drone))

        running_tasks = [print_mission_progress_task]
        termination_task = asyncio.ensure_future(
            observe_is_in_air(drone, running_tasks))

        mission_items = []
        mission_items.append(MissionItem(39.08554166955255,
                                        121.80813517598546,
                                        2,
                                        1,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan'),
                                        float('nan'),
                                        float('nan'),
                                        float('nan')))
        mission_items.append(MissionItem(39.08520097384079,
                                        121.8083480191318,
                                        2,
                                        1,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan'),
                                        float('nan'),
                                        float('nan'),
                                        float('nan')))
        mission_items.append(MissionItem(39.08554166955255,
                                        121.80813517598546,
                                        2,
                                        1,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan'),
                                        float('nan'),
                                        float('nan'),
                                        float('nan')))
        mission_items.append(MissionItem(39.08520097384079,
                                        121.8083480191318,
                                        2,
                                        1,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan'),
                                        float('nan'),
                                        float('nan'),
                                        float('nan')))

        mission_plan = MissionPlan(mission_items)

        await drone.mission.set_return_to_launch_after_mission(True)

        print("-- Uploading mission")
        await drone.mission.upload_mission(mission_plan)

        print("-- Arming")
        await drone.action.arm()

        print("-- Starting mission")
        await drone.mission.start_mission()

        await termination_task

        # await drone.action.return_to_launch()

        await drone.action.land()



    async def print_mission_progress(self,drone):
        async for mission_progress in drone.mission.mission_progress():
            print(f"Mission progress: "
                f"{mission_progress.current}/"
                f"{mission_progress.total}")


    async def observe_is_in_air(self,drone, running_tasks):
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


# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())