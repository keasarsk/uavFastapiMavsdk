from sqlalchemy.orm import Session
from DataBase.database import flylogtest, drone_flylog
from mavsdk import System
import time
import datetime

def get_test(session: Session):
    print("dataintodb get_test yes")
    print(session.query(flylogtest).first())
    fl = flylogtest(order_id = 7)
    session.add(fl)
    session.commit()
    print("get_test yes")
    print(session.query(flylogtest).first())

def get_drone_flylog(session: Session):
    print("get_drone_flylog yes")
    print(session.query(drone_flylog).first())

def insert_log_localmysql(session: Session, times: int, gap: int):
    # ---------test
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
    # async for flight_mode in drone.telemetry.flight_mode():
    #	print(type(flight_mode))#<enum 'FlightMode>
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
        for is_in_air in drone.telemetry.in_air():
            iia = is_in_air

        print(iia, la, ln, bat, flm, ia, datetime.now())
        log = drone_flylog(drone_number="1", in_air=iia, lat = la, lng = ln, battery = bat, flight_mode = flm, is_armed = ia, datetime=datetime.now())
        session.add(log)
        session.commit()
