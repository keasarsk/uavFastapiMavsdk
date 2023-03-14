from mavsdk import System
import time
from datetime import datetime
import asyncio


async def run():
    with open("../log2.txt","r") as log:
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
    
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
