from uasyncio import asyncio


async def main():
    while True:
        await asyncio.sleep_ms(10)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(e))
finally:
    asyncio.new_event_loop()
