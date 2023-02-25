import asyncio
from mavsdk import System
import time

async def run():
    print("test yes")
    drone = System()
    drone.connect(system_address="tcp://192.168.1.191:8080")

    print("Waiting for drone to connect...")
    for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    print("Waiting for drone to have a global position estimate...")
    for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break
    
    # await drone.action.arm()

    print("lat")
    print(drone.telemetry.position()['latitude_deg'])
    print("lng")
    print(drone.telemetry.position()['longitude_deg'])
    print("batt")
    print(drone.telemetry.battery()['remaining_percent'])
    # la = drone.telemetry.position()['latitude_deg']
    # ln = drone.telemetry.position()['longitude_deg']
    # bat = drone.telemetry.battery()['remaining_percent']
    print("------flight_mode:")
    for flight_mode in drone.telemetry.flight_mode():
        print("FlightMode:", flight_mode)
    print("--------is_armed:")
    for is_armed in drone.telemetry.armed():
        print("Is_armed:", is_armed)
    print("--------is_in_air:")
    for is_in_air in drone.telemetry.in_air():
        print("Is_in_air:", is_in_air)

        

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())