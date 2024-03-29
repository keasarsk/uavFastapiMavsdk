from mavsdk import System
import time
from datetime import datetime
import asyncio


from fastapi import Depends
import DataBase.crud, DataBase.schemad
from DataBase.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine) #数据库初始化，如果没有库或者表，会自动创建
# Dependency
def get_db():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

async def run(session: Session = Depends(get_db)):
    
    print("insert into local mysql")
    drone = System()
    await drone.connect(system_address="tcp://192.168.1.191:8080")
    #  await drone.connect(system_address="udp://:14540")

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
    times = 10000
    gap = 1
    while(times > 0):
        times -= 1
        time.sleep(0.5)
        async for i in drone.telemetry.position():
            la = i.latitude_deg
            ln = i.longitude_deg
            break
        async for i in drone.telemetry.battery():
            bat = i.remaining_percent
            break
        async for flight_mode in drone.telemetry.flight_mode():
            flm = flight_mode
            break
        async for is_armed in drone.telemetry.armed():
            ia = is_armed
            break
        async for is_in_air in drone.telemetry.in_air():
            iia = is_in_air
            break

        print(iia, la, ln, bat, flm, ia, datetime.now())
        
        log = drone_flylog(drone_number="1", in_air=iia, lat = la, lng = ln, battery = bat, flight_mode = flm, is_armed = ia, datetime=datetime.now())
        
        # session.add(log)
        # session.commit()
        
    
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
