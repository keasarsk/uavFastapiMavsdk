
from fastapi import FastAPI
import os
import sys

from pydantic import BaseModel

app = FastAPI()

# = None ,means default


@app.get("/test")
async def test():
    print("---------------tesst:")
    if os.system('python test.py'):
        return False
    else:
        return True


# 3.15 实机任务测试
@app.get("/missiontest")
async def test():
    print("---------------missiontest:")
    if os.system('python missiontest.py'):
        return False
    else:
        return True




@app.get("/armAll")
async def armAll():
    print("---------------arm all uav:")
    if os.system('python uav_all_test.py'):
        return False
    else:
        return True

class uav_info(BaseModel):
    uav: str
    def get_uav_info(self):
        uav_num = self.uav
        return uav_num[-1]

@app.get("/{uav_num}/fly/takeoff")
async def takeoff(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python takeoff.py ' + uav_port):
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

class MissionItems(BaseModel):
    routeLine = []
    altitude: str
    camera: str
    speed_m_s = []
    camera_photo_interval_s = []
    yaw_deg = []
    camera_action = []
    relative_altitude_m = []
    def get_info(self):
        latitude_deg = []
        longitude_deg = []

        for i in self.routeLine:
            # dictA = i
            latitude_deg.append(i['lat'])
            longitude_deg.append(i['lng'])

        print("self.altitude[:-1]",self.altitude[:-1])
        altitude_num = float(self.altitude[:-1])
        self.relative_altitude_m.append(altitude_num)
        self.camera_action.append(self.camera)
        camera_photo_interval_s = self.camera_photo_interval_s
        yaw_deg = self.yaw_deg
        return latitude_deg,longitude_deg,self.relative_altitude_m,\
               self.speed_m_s,self.camera_action,camera_photo_interval_s,yaw_deg

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
@app.post("/{uav_num}/mission")
async def mission(uav_num: str,missionItems: MissionItems):
    uav_port = str(int(uav_num[-1]) + 14540)

    # print("type(missionItems.routeLine):",type(missionItems.routeLine),missionItems.routeLine)
    # print("type(missionItems.routeLine[1]):", type(missionItems.routeLine[1]), missionItems.routeLine[1])
    # itemsss = list(missionItems.get_info())
    # print("type(missionItems)",type(missionItems.get_info()),missionItems.get_info())
    itemsss = missionItems.get_info()
    print("itemsss:", itemsss)

    # writter into mission_items.txt
    with  open('mission_items.txt', 'w') as mission_items_txt:
        for i in itemsss:
            i = str(i)
            mission_items_txt.write(i + '\n')
        mission_items_txt.close()

    if os.system('python mission2.py ' + uav_port):
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
    if os.system('python missiontest2.py '):
        return False
    else:
        return True



@app.get("/{uav_num}/fly/land")
async def land(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 land.py ' + uav_port):
        return False
    else:
        return True

@app.get("/{uav_num}/keyboardControl")
async def keyboardControl(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 keyboardControl.py ' + uav_port):
        return False
    else:
        return True


@app.get("/{uav_num}/shutdown")
async def shutdown(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 shutdown.py ' + uav_port):
        return False
    else:
        return True


@app.get("/{uav_num}/logfile")
async def logfile(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 logfile.py ' + uav_port):
        return False
    else:
        return True


@app.get("/{uav_num}/returntolaunch")
async def returntolaunch(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 return_to_launch.py ' + uav_port):
        return False
    else:
        return True


@app.get("/{uav_num}/goto")
async def goto(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 goto.py ' + uav_port):
        return False
    else:
        return True


@app.get("/{uav_num}/followme")
async def followme(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 followme.py ' + uav_port):
        return False
    else:
        return True


@app.get("/{uav_num}/location")
async def location(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 location_now.py ' + uav_port):
        return False
    else:
        return True


@app.get("/{uav_num}/camera")
async def camera(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 camera.py ' + uav_port):
        return False
    else:
        return True


@app.get("/{uav_num}/manualcontrol")
async def manualcontrol(uav_num: str):
    uav_port = str(int(uav_num[-1]) + 14540)
    if os.system('python3 manual_control.py ' + uav_port):
        return False
    else:
        return True



# --------------------auto disarming
# # @app.get("/disarm")
# async def root():
#     finish = False
#     if os.system('python3 disarm.py'):
#         finish = True
#
#     return finish


# @app.get("/sleep/")
# async def root():
#     return dictA


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
