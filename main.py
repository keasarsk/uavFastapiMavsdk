
# from __future__ import all_feature_names
# from msilib.schema import tables
# import imp
from operator import truediv
import os

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from numpy import double
# import sys
from pydantic import BaseModel


app = FastAPI()

# 写个主页面
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>UAVFastAPI主页面</h1>
        <!--发送websocket-->
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <form action=" onsubmit="getsitllog(event)">
            <button>点击获取sitl的日志</button>
        
        </form>
        <!--展示websocket-->
        <ul id='messages'>
        </ul>

        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }

        </script>
    </body>
</html>
"""
@app.get("/")
async def get():
    return HTMLResponse(html)


# class MissionItems(BaseModel):
#     routeLine = []
#     altitude: float
#     camera: str
#     speed_m_s = []
#     camera_photo_interval_s = []
#     yaw_deg = []
#     camera_action = []
#     relative_altitude_m = []
#     def get_info(self):
#         latitude_deg = []
#         longitude_deg = []

#         for i in self.routeLine:
#             # dictA = i
#             latitude_deg.append(i['lat'])
#             longitude_deg.append(i['lng'])

#         print("self.altitude[:-1]",self.altitude[:-1])
#         altitude_num = float(self.altitude[:-1])
#         self.relative_altitude_m.append(altitude_num)
#         self.camera_action.append(self.camera)
#         camera_photo_interval_s = self.camera_photo_interval_s
#         yaw_deg = self.yaw_deg
#         return latitude_deg,longitude_deg,self.relative_altitude_m,\
#                self.speed_m_s,self.camera_action,camera_photo_interval_s,yaw_deg

# 按照师姐写
class MissionItems(BaseModel):
    # 经纬度列表 double
    lat = []
    lon = []
    # 相对高度列表 float
    relative_altitude_m = []
    # 飞行速度列表 float
    speed_m_s = []
    # 飞过还是停在航点列表 bool
    is_fly_through = []
    # 任务点触发的相机动作列表 CameraAction:
    camera_action = []
    # 停留时间列表 float
    loiter_time_s = []
    
    def getInfo(self):
        return self.lat , self.lon , self.relative_altitude_m , self.speed_m_s , self.is_fly_through , self.camera_action , self.loiter_time_s
    

# 4.17 链接小飞机试试
# 失败
@app.get("/little")
async def test():
    print("---------------little:")
    if os.system('python little.py'):
        return False
    else:
        return True






# 仿真全部arm
from uav_all_test import uav_all_test
allarm = uav_all_test()
@app.get("/armAll")
async def armAll():
    print("---------------arm all uav:")
    if await allarm.run():
        # if os.system('python3 uav_all_test.py'):
        return False
    else:
        return True




# 仿真takeoff
from takeoff import takeoff
tkoff = takeoff()
@app.get("/{uav_num}/sitl/takeoff")
async def takeoff(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    # if os.system('python takeoff.py ' + uav_port):
    if await tkoff.run():
        return False
    else:
        return True


# -------------------sys.argv------------------
# class Item(BaseModel):
#     name: str
#     description: str = None
#     price: float
#     tax: float = None
#     def get_item(self):
#         name = self.name
#         description = self.description
#         price = self.price
#         tax = self.tax
#         return name,description,price,tax
# @app.post("/uav0/systest")
# async def systest(item: Item):
#     # print(type(item))
#     itemsss = list(item.get_item())
#     # print(itemsss)
#     # print(type(itemsss))
#     print("itemsss[0],itemsss[1]:",itemsss[0],itemsss[1])
#     print(111)
#     if os.system('python3 ./uav0/systest.py '+ itemsss[0]):
#         finish = False
#     else:
#         finish = True
#     return finish

# -------------------mission_items------------------


    # 行得通的简易版:
    # json:
    # {
    #     "speed_m_s": [2],
    #     "latitude_deg": [39.086536650135685, 39.086536650135685],
    #     "longitude_deg": [121.81313931941986, 121.81313931941986],
    #     "relative_altitude_m": [3]
    # }
    # speed_m_s = []
    # latitude_deg = []
    # longitude_deg = []
    # relative_altitude_m = []
    #
    # def get_info(self):
    #     # uav_num = self.uav
    #     latitude_deg = self.latitude_deg
    #     longitude_deg = self.longitude_deg
    #     relative_altitude_m = self.relative_altitude_m
    #     speed_m_s = self.speed_m_s
    #     return latitude_deg, longitude_deg, relative_altitude_m, speed_m_s
    


# 3.15 实机任务测试
# 80大无人机 死命令
from bigmissiontest import bigmissiontest
bigmissionT = bigmissiontest()
@app.get("/missiontest")
async def missiontest():
    print("---------------bigmissiontest:")
    # if os.system('python missiontest.py'):
    if await bigmissionT.run():
        return False
    else:
        return True


# 3.15 实机测试mission 把任务写进文件
@app.post("/missiontest2")
async def mission(uav_num: str,missionItems: MissionItems):
    uav_port = str(int(uav_num[-1]) + 14540)

    itemsss = missionItems.get_info()

    # writter into mission_items.txt
    with  open('mission_items.txt', 'w') as mission_items_txt:
        for i in itemsss:
            i = str(i)
            mission_items_txt.write(i + '\n')
        mission_items_txt.close()

    print("---------------missiontest2222:")
    if os.system('python bigmissiontest.py '):
        return False
    else:
        return True



# 仿真land
from land import land
lad = land()
@app.get("/{uav_num}/sitl/land")
async def land(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    # if os.system('python3 land.py ' + uav_port):
    if await lad.run():
        return False
    else:
        return True

# 好像并没有什么用
@app.get("/{uav_num}/keyboardControl")
async def keyboardControl(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 keyboardControl.py ' + uav_port):
        return False
    else:
        return True

# 这个也不能轻易用
# @app.get("/{uav_num}/shutdown")
# async def shutdown(uav_num: str):
#     uav_port = str(int(uav_num[-1]) + 14540)
#     if os.system('python3 shutdown.py ' + uav_port):
#         return False
#     else:
#         return True


# 下载日志文件 这个现在下载在了本地
@app.get("/{uav_num}/logfile")
async def logfile(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 logfile.py ' + uav_port):
        return False
    else:
        return True


# 升高的一定高度 返回发射位置并着陆
from return_to_launch import returntolaunch

returnlaunch = returntolaunch()
@app.get("/{uav_num}/returntolaunch")
async def relaunch(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    # if os.system('python3 return_to_launch.py ' + uav_port):
    if await returnlaunch.run():
        return False
    else:
        return True


# 需要传入一个坐标 未完善
from goto import goto

gt = goto()
@app.get("/{uav_num}/goto")
async def gto(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    # if os.system('python3 goto.py ' + uav_port):
    if await gt.run():
        return False
    else:
        return True

# 未完善 暂时意义不大
@app.get("/{uav_num}/followme")
async def followme(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 followme.py ' + uav_port):
        return False
    else:
        return True







# @app.get("/{uav_num}/location")
# async def location(uav_num: str):
    
#     uav_port = str(int(uav_num[-1]) + 14540)
#     if os.system('python3 location_now.py ' + uav_port):
#         return False
#     else:
#         return True


# 这个等推流吧
@app.get("/{uav_num}/camera")
async def camera(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 camera.py ' + uav_port):
        return False
    else:
        return True

# 意义不大
@app.get("/{uav_num}/manualcontrol")
async def manualcontrol(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 manual_control.py ' + uav_port):
        return False
    else:
        return True



# 4.18
# 4.18 大无人机日志
from Location_log import Location_log
log = Location_log()
@app.get("/{uav_num}/biglog")
async def location(uav_num: str):
    if uav_num =="1" :
        uav_port = "192.168.1.81:8080"
    elif uav_num == "2" :
        uav_port = "192.168.1.191:8080"
    log.uavport = uav_port
    # print("log.uavport-----")
    print(log.uavport)
    if await log.run():
        return log.battery , log.location
    else:
        return log.battery , log.location



# 4.19
# 仿真任务测试json
from missionsitl import msitl
misitl = msitl()
from mavsdk.mission import MissionItem
@app.post("/{uav_num}/sitlmission")
async def mission(uav_num: str,missionItems: MissionItems):
    uav_port = str(int(uav_num[-1]) + 14540)
    misitl.uavport = uav_port
    # 获得传进来的json内容
    print("missionItems.lat-------",missionItems.lat)
    print("missionItems.lat[0]-------",missionItems.lat[0])
    # 在这里就把数据转成MissionItem格式
    missionItemlistmain = []
    i = 0
    while (i<len(missionItems.lat)):
        missionItemlistmain.append(MissionItem(double(missionItems.lat[i]),
                                                double(missionItems.lon[0]),
                                                float(missionItems.relative_altitude_m[i]),
                                                float(missionItems.speed_m_s[i]),
                                                bool(missionItems.is_fly_through[i]),
                                                float('nan'),
                                                float('nan'),
                                                MissionItem.CameraAction.NONE,
                                                float(missionItems.loiter_time_s[i]),
                                                float('nan'),
                                                float('nan'),
                                                float('nan')
                                                ))
        print("missionItemlistmain[i]" , missionItemlistmain[i])
        i += 1
    # 赋值给misitl.missionItemlist
    misitl.missionItemlist = missionItemlistmain
    if await misitl.run():
        return False
    else:
        return True


# 4.20 arm大无人机
from bigarm import big
al = big()
@app.get("/bigarmall")
async def bigarm():
    print("---------------arm bigbigbig:")
    if await al.run():
        # if os.system('python3 uav_all_test.py'):
        return False
    else:
        return True


# 4.20 实机任务测试json
# 大无人机任务测试json
from missionbigjson import missionbigjson
missbig = missionbigjson()
@app.post("/{uav_num}/missionbigjson")
async def mission(uav_num: str,missionItems: MissionItems):
    if uav_num =="1" :
        uav_port = "192.168.1.81:8080"
    elif uav_num == "2" :
        uav_port = "192.168.1.191:8080"
    # uav_port = "192.168.1.191:8080"
    print(uav_port)
    missbig.uavport = uav_port
    print("missbig.uavport---------",missbig.uavport)
    # 在这里就把数据转成MissionItem格式
    missionItemlistmain = []
    i = 0
    while (i<len(missionItems.lat)):
        missionItemlistmain.append(MissionItem(double(missionItems.lat[i]),
                                                double(missionItems.lon[i]),
                                                float(missionItems.relative_altitude_m[i]),
                                                float(missionItems.speed_m_s[i]),
                                                bool(missionItems.is_fly_through[i]),
                                                float('nan'),
                                                float('nan'),
                                                MissionItem.CameraAction.NONE,
                                                float(missionItems.loiter_time_s[i]),
                                                float('nan'),
                                                float('nan'),
                                                float('nan'),
                                                float('nan')
                                                ))
        print("missionItemlistmain[i]" , missionItemlistmain[i])
        i += 1
    # 赋值给missbig.missionItemlist
    missbig.missionItemlist = missionItemlistmain
    print("missbig.missionItemlist-------",missbig.missionItemlist)
    # return True
    if await missbig.run():
        return False
    else:
        return True


# 4.21 暂停任务
from pausemission import pausemission
psm = pausemission()
@app.get("/{uav_num}/pausemission")
async def psmission(uav_num: str):
    if uav_num =="1" :
        uav_port = "192.168.1.81:8080"
    elif uav_num == "2" :
        uav_port = "192.168.1.191:8080"
    psm.uavport = uav_port
    if await psm.run():
        return False
    else:
        return True

# 4.21 启动任务
from startmission import startmission
stm = startmission()
@app.get("/{uav_num}/startmission")
async def stmission(uav_num: str):
    if uav_num =="1" :
        uav_port = "192.168.1.81:8080"
    elif uav_num == "2" :
        uav_port = "192.168.1.191:8080"
    stm.uavport = uav_port
    if await stm.run():
        return False
    else:
        return True

# 4.21 终止任务并返航
from terminationreturn import terminationreturn
terreturn = terminationreturn()
@app.get("/{uav_num}/terminationreturn")
async def tereturn(uav_num: str):
    if uav_num =="1" :
        uav_port = "192.168.1.81:8080"
    elif uav_num == "2" :
        uav_port = "192.168.1.191:8080"
    terreturn.uavport = uav_port
    if await terreturn.run():
        return False
    else:
        return True


# 仿真无人机日志websocket实现
from sitllogsocket import sitllogsocket
sitllogsk = sitllogsocket()
# @app.websocket("/{uav_num}/sitllogsocket")
@app.websocket("/ws")
# async def logsocket(uav_num: str , websocketfront: WebSocket):
async def wssocket(websocketfront: WebSocket):
    # uav_port = str(int(uav_num[-1]) + 14540)
    # sitllogsk.uavport = uav_port
    sitllogsk.uavport = 14541
    sitllogsk.websocket = websocketfront

    # # 可以------------
    # await websocketfront.accept()
    # while True:
    #     data = "12345"
    #     await websocketfront.send_text(f"Message text was: 1234")
    # # --------------

    if await sitllogsk.run():
        return True
    else:
        return False


# 4.22 大无人机日志的websocket实现
from biglogsocket import biglogsocket
biglogsk = biglogsocket()
@app.websocket("/{uav_num}/biglogsocket")
async def biglogsok(uav_num: str,bigwebsocket : WebSocket):
    if uav_num =="1" :
        uav_port = "192.168.1.81:8080"
    elif uav_num == "2" :
        uav_port = "192.168.1.191:8080"
    biglogsk.uavport = uav_port
    biglogsk.websocket = bigwebsocket

    await biglogsk.run()





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
