
import asyncio
from curses.ascii import alt

async def run():
    # with open('mission_items.txt','r') as f:
    #     for i,line in enumerate(f):
    #         line = line[1:-2]
    #         print(len(line))
    #         print('line',line)
    #         print('typeline',type(line))
    #         linearray=line.split(',')
    #         print('len(linearray)',len(linearray))

    #         # print('i',i)
    #         print('linearray[0]',linearray[0])
    #         print('linearray[0]',linearray[1])
    #         # print(linearray[1])

    #         latlist = []
    lonlist = []
    altlist = []
    missionnum = 0
    with open('mission_items.txt','r') as f:
        for i,line in enumerate(f):
            line = line[1:-2]
            linearray=line.split(',')
            missionnum = len(linearray)
            if i == 0 :
                latlist = linearray
            elif i == 1 :
                lonlist = linearray
            elif i == 2 :
                altlist = linearray

    # print('latlist[0]',latlist[0])
    # print(altlist[0])
    j = 0
    while j < missionnum :
        print('latlist[]',latlist[j])
        print('lonlist[]',lonlist[j])
        print('altlist[]',altlist[j])
        # print("j",j)
        j += 1
        

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())