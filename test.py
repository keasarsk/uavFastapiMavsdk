import asyncio
from mavsdk import System
import time

async def run():
    print("test yes")
    drone = System()
    # drone.connect(system_address="tcp://192.168.1.191:8080")
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break
    
    # await drone.action.arm()

    # print("lat")
    # print(await drone.telemetry.position()['latitude_deg'])
    #print(type(drone.telemetry.position()))# <class 'async_generator'>
    #async for i in drone.telemetry.position():
    #	print(i.latitude_deg)# yes
    #	print(type(i))# bool

    # la = drone.telemetry.position()['latitude_deg']
    # ln = drone.telemetry.position()['longitude_deg']
    # bat = drone.telemetry.battery()['remaining_percent']
    #print("------flight_mode:")
    # FlightMode: HOLD
    async for flight_mode in drone.telemetry.flight_mode():
    	print(type(flight_mode))#<enum 'FlightMode>
    #    print("FlightMode:", flight_mode)
    
    #print("--------is_armed:")
    #Is_armed: False
    #print(type(drone.telemetry.armed()))# <class 'async_generator'>
    #async for is_armed in drone.telemetry.armed():
    #	print(type(is_armed))# bool
    #	print("Is_armed:", is_armed)
    #print("--------is_in_air:")
    #print(type(drone.telemetry.in_air()))# <class 'async_generator'>
    #Is_in_air: False
    #async for is_in_air in drone.telemetry.in_air():
    #    print("Is_in_air:", is_in_air)

        

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
