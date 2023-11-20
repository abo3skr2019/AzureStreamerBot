import asyncio
import websockets


async def test_ws():
    uri = "ws://127.0.0.1:5000/ws"  # replace with your server's URI
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, server!")
        response = await websocket.recv()
        print(f"Received from server: {response}")


if __name__ == "__main__":
    asyncio.run(test_ws())
