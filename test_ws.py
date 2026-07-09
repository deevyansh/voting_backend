import asyncio
import websockets

async def listen():
    async with websockets.connect("ws://127.0.0.1:8000/wb") as ws:
        print("Connected! Waiting for broadcasts...")
        while True:
            message = await ws.recv()
            print("Received:", message)

asyncio.run(listen())