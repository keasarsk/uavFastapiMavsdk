from sqlalchemy.orm import Session
from DataBase.database import flylogtest, drone_flylog
from mavsdk import System
import time

def get_test(session: Session):
    print("dataintodb get_test yes")
    print(session.query(flylogtest).first())
    fl = flylogtest(order_id = )
    session.add(fl)
    session.commit()
    print("get_test yes")
    print(session.query(flylogtest).first())

def get_drone_flylog(session: Session):
    print("get_drone_flylog yes")
    print(session.query(drone_flylog).first())

# def insert_log(session: Session, times: int, gap: int):
#     print("insert into log")
#     drone = System()
#     drone.connect(system_address="tcp://192.168.1.191:8080")

#     print("Waiting for drone to connect...")
#     for state in drone.core.connection_state():
#         if state.is_connected:
#             print(f"Drone discovered!")
#             break

#     print("Waiting for drone to have a global position estimate...")
#     for health in drone.telemetry.health():
#         if health.is_global_position_ok:
#             print("Global position estimate ok")
#             break
    
#     while(times > 0):
#         times -= 1
#         time.sleep(gap)
#         la = drone.telemetry.position()['latitude_deg']
#         ln = drone.telemetry.position()['longitude_deg']
#         bat = drone.telemetry.battery()['remaining_percent']
#         async for flight_mode in drone.telemetry.flight_mode():
#             print("FlightMode:", flight_mode)
#         async for is_armed in drone.telemetry.armed():
#             print("Is_armed:", is_armed)
#         async for is_in_air in drone.telemetry.in_air():
#             print("Is_in_air:", is_in_air)


#         log = drone_flylog(drone_number="1", in_air=, lat = la, lng = ln, battery = bat, flight_mode = "str", is_armed = 1, datetime=datetime.now())
#         session.add(log)
#         session.commit()
