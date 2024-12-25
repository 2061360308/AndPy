#!/usr/bin/env python

import asyncio
from websockets import serve


async def echo(websocket):
    print(websocket.request.path)
    async for message in websocket:
        await websocket.send(f"Path: Message: {message}")


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever


asyncio.run(main())
