# Concurrently breakfast
import asyncio
from time import sleep, time


async def make_coffee(): # 1
    print("coffee: prepare ingridients")
    sleep(1)
    print("coffee: waiting...")
    await asyncio.sleep(5) # 2 : pause, another tasks can be run
    print("coffee: ready")

async def fry_eggs(): # 1
    print("eggs: prepare ingridients")
    sleep(1)
    print("eggs: frying...")
    await asyncio.sleep(3) # 2 : pause, another tasks can be run
    print("eggs: ready")

async def main():
    start = time()
    coffee = asyncio.create_task(make_coffee())
    egg = asyncio.create_task(fry_eggs())
    await coffee
    await egg
    print(f"breakfast is ready in {time()-start} min")


asyncio.run(main()) # run top level function concurrently