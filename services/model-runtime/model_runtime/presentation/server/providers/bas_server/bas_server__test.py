import unittest
from model_runtime.util.runtime.deasync import deasync
from .bas_server import BasServer
import asyncio
from websockets.client import connect

class TestBasServer(unittest.TestCase):
    
    @deasync
    async def test_bas_server_serves(self):
        
        server = BasServer()
        await server.bas.prompt("Figure out a good marketing strategy for my brand new recruitment firm.")
        
        async def bg_serve():
            server.serve()
            
        task = asyncio.create_task(bg_serve())
        
        i = 0
        async for summary in server.bas.get_summary_stream():
            print(i, summary)
            i += 1
            if i > 3:
                break
        
        task.cancel()
        
    @deasync
    async def test_bas_server_connects(self):
        
        server = BasServer()
        await server.bas.prompt("Figure out a good marketing strategy for my brand new recruitment firm.")
        
        async def bg_serve():
            server.serve()
            
        task = asyncio.create_task(bg_serve())
        
        await asyncio.sleep(3)
        async with connect("ws://0.0.0.0:8000/summary") as websocket:
            while True:
                message = await websocket.recv()
                print(message)
                await asyncio.sleep(.5)
            
            
            