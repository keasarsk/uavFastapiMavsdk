import asyncio
from mavsdk import System

class biguavtest():
    async def run():

        print("Waiting...")

        drone = System()
        await drone.connect(system_address="tcp://192.168.1.81:8080")

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered!")
                break

        # print("Waiting for drone to have a global position estimate...")
        # async for health in drone.telemetry.health():
        #     if health.is_global_position_ok:
        #         print("Global position estimate ok")
        #         break

        print("-- Arming")
        await drone.action.arm()
        await drone.action.land()

        await asyncio.sleep(5)

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(run())
