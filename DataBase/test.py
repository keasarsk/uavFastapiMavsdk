# is_inair  is_armed
async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    asyncio.ensure_future(print_is_armed(drone))
    asyncio.ensure_future(print_is_in_air(drone))


async def print_is_armed(drone):
    async for is_armed in drone.telemetry.armed():
        print("Is_armed:", is_armed)


async def print_is_in_air(drone):
    async for is_in_air in drone.telemetry.in_air():
        print("Is_in_air:", is_in_air)

# flight_mode
async def print_flight_mode():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    async for flight_mode in drone.telemetry.flight_mode():
        print("FlightMode:", flight_mode)