# python2 path.....
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
def arm_and_takeoff(aTargetAltitude):
    vehicle = connect('10.42.0.62:14550', wait_ready=True, baud=921600)

    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

        
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True    

    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)

    
    # me
    if vehicle.armed:
        print("arm!!!")