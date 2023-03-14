#!/usr/bin/env python3
# 对应 api: @app.get("/logtest2")
# 读取 log.txt 文件, 字符串处理成数据库表 drone_flylog对应格式后 session.add 和 session.commit

from sqlalchemy.orm import Session
from DataBase.database import drone_flylog
from mavsdk import System
from datetime import datetime

class locallogtxtintodb():
    def get_test(self, session: Session):
        print("locallogtxtintodb start")
        count = 200
        with open("log.txt","r") as log:
            for line in log.readlines():
                line = line.lstrip('[')
                line = line.rstrip(']')
                arr = line.split(', ')
                # print(arr[0])
                # print(arr[2])
                if arr[0] == 'True': iia = 1
                else : iia = 0
                la = (float)(arr[1])
                ln = (float)(arr[2])
                bat = (float)(arr[3])
                flm = arr[4].lstrip('<FlightMode.')
                flm = flm.rstrip('>')
                if arr[5] == 'True': ia = 1
                else : ia = 0
                
                timeyear = arr[6].lstrip('datetime.datetime(')
                t = datetime(int(timeyear),int(arr[7]),int(arr[8]),int(arr[9]),int(arr[10]),int(arr[11]))
                
                print(iia, la, ln, bat, flm, ia, t)
                logsingle = drone_flylog(id=count, drone_number=1, in_air=iia, lat=la, lng=ln, battery=bat,flight_mode=flm, is_armed=ia, datetime=t)
                count += 1
                session.add(logsingle)
        session.commit()
        session.close()
        print("locallogtxtintodb end")

