#!/usr/bin/env python3

"""
This example shows how to use the manual controls plugin.

Note: Manual inputs are taken from a test set in this example to decrease complexity. Manual inputs
can be received from devices such as a joystick using third-party python extensions
在本例中，手动输入来自测试集，以降低复杂性。可以使用第三方python扩展从设备(如操纵杆)接收手动输入
Note: Taking off the drone is not necessary before enabling manual inputs. It is acceptable to send
positive throttle input to leave the ground. Takeoff is used in this example to decrease complexity
在启用手动输入之前，没有必要起飞无人机。它是可以接受的送积极油门输入离开地面。本例中使用起飞来降低复杂性
"""

import asyncio
import random
from mavsdk import System
import sys
# Test set of manual inputs. Format: [roll, pitch, throttle, yaw]
manual_inputs = [
    [0, 0, 0.5, 0],  # no movement
    [-1, 0, 0.5, 0],  # minimum roll
    [1, 0, 0.5, 0],  # maximum roll
    [0, -1, 0.5, 0],  # minimum pitch
    [0, 1, 0.5, 0],  # maximum pitch
    [0, 0, 0.5, -1],  # minimum yaw
    [0, 0, 0.5, 1],  # maximum yaw
    [0, 0, 1, 0],  # max throttle
    [0, 0, 0, 0],  # minimum throttle
]


async def manual_controls():
    """Main function to connect to the drone and input manual controls"""
    # Connect to the Simulation
    drone = System()
    await drone.connect(system_address="udp://:" + sys.argv[1])

    # This waits till a mavlink based drone is connected
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    # Checking if Global Position Estimate is ok
    async for global_lock in drone.telemetry.health():
        if global_lock.is_global_position_ok:
            print("-- Global position state is ok")
            break

    # set the manual control input after arming
    await drone.manual_control.set_manual_control_input(
        float(0), float(0), float(0.5), float(0)
    )

    # Arming the drone
    print("-- Arming")
    await drone.action.arm()

    # Takeoff the vehicle
    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    # set the manual control input after arming
    await drone.manual_control.set_manual_control_input(
        float(0), float(0), float(0.5), float(0)
    )

    # start manual control
    print("-- Starting manual control")
    await drone.manual_control.start_position_control()

    while True:
        # grabs a random input from the test list
        # WARNING - your simulation vehicle may crash if its unlucky enough
        input_index = random.randint(0, len(manual_inputs) - 1)
        input_list = manual_inputs[input_index]

        # get current state of roll axis (between -1 and 1)
        roll = float(input_list[0])
        # get current state of pitch axis (between -1 and 1)
        pitch = float(input_list[1])
        # get current state of throttle axis (between -1 and 1, but between 0 and 1 is expected)
        throttle = float(input_list[2])
        # get current state of yaw axis (between -1 and 1)
        yaw = float(input_list[3])

        await drone.manual_control.set_manual_control_input(roll, pitch, throttle, yaw)

        await asyncio.sleep(0.1)




loop = asyncio.get_event_loop()
loop.run_until_complete(manual_controls())
