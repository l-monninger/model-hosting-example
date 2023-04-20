import unittest
from model_sidecar.util.runtime.deasync import deasync
from .model_manager_server import ModelManagerServer
import asyncio
from websockets.client import connect
from model_sidecar.util.model_config import ModelConfig
import json

class TestModelManagersServer(unittest.TestCase):
    
    @deasync
    async def test_runs_output_manager(self):
        
        server = ModelManagerServer(latency=2) 
        
        async def bg_serve():
            server.serve()
        
        task = asyncio.create_task(bg_serve())
        async def pstuff(val):
            print(val)  
            
        await asyncio.sleep(4)
        await server.subscribe_out_buff(pstuff)
        server.out_buff.put((1, "Hello"))
        
        await asyncio.wait_for(task, timeout=20)
        
    
    @deasync
    async def test_tf_sidecar_server_serves(self):
        
        server = ModelManagerServer(latency=2)    
        async def pstuff(val):
            print(val)  
            
        await server.subscribe_out_buff(pstuff)
        
        async def bg_serve():
            server.serve()
            
        task = asyncio.create_task(bg_serve())
    
        async def client():
            await asyncio.sleep(3)
            async with connect("ws://0.0.0.0:8000/destroy") as websocket:
                while True:
                    message = await websocket.recv()
                    print(message)
                    await asyncio.sleep(.5)
                
        await asyncio.gather(
            asyncio.wait_for(task, timeout=20),
            client()
        )
        
    @deasync
    async def test_tf_sidecar_server_external(self):
        
        server = ModelManagerServer(latency=2)    
        async def pstuff(val):
            print(val)  
            
        await server.subscribe_out_buff(pstuff)
        
        async def bg_serve():
            server.serve()
            
        task = asyncio.create_task(bg_serve())
    
        await asyncio.wait_for(task, timeout=20),
        
            

            