from mavsdk import System
import time
import datetime

def insert_log_localmysql(times: int, gap: int):

    print("insert into local mysql")
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
    
    while(times > 0):
        times -= 1
        time.sleep(gap)
        for i in drone.telemetry.position():
            la = i.latitude_deg
            ln = i.longitude_deg
            bat = i.remaining_percent
            break
        for flight_mode in drone.telemetry.flight_mode():
            flm = flight_mode
            break
        for is_armed in drone.telemetry.armed():
            ia = is_armed
            break
        for is_in_air in drone.telemetry.in_air():
            iia = is_in_air
            break

        print(iia, la, ln, bat, flm, ia, datetime.now())
        # log = drone_flylog(drone_number="1", in_air=iia, lat = la, lng = ln, battery = bat, flight_mode = flm, is_armed = ia, datetime=datetime.now())
        # session.add(log)
        # session.commit()
        

if __name__ == "__main__":
    insert_log_localmysql(5, 1)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(run())
