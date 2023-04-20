from ...server import Server
from model_sidecar.util.subprocess import StdFd
from model_sidecar.util.model_config import ModelConfig
from model_sidecar.logic.model_manager import ModelManager
from model_sidecar.logic.model_manager.providers.tf_model_manager import TfModelManager
from fastapi import FastAPI, WebSocketDisconnect, WebSocket
import uvicorn
import nest_asyncio
from weakref import WeakSet, getweakrefcount, ref
from typing import Callable, Awaitable, Iterable, Optional, Tuple, AsyncIterator
from queue import Queue, Empty
import asyncio
import json
from signal import SIGINT, SIGTERM
from fastapi.middleware.cors import CORSMiddleware
nest_asyncio.apply()


class ModelManagerServer(Server):
    
    manager : ModelManager[ModelConfig]
    app : FastAPI
    
    latency : float
    
    action_buff_lock : asyncio.Lock
    action_buff : Queue[Callable[[], AsyncIterator[Tuple[StdFd, str]]]]
    
    out_buff_lock : asyncio.Lock
    out_buff : Queue[Tuple[StdFd, str]]
    
    out_cbs_lock : asyncio.Lock
    out_cbs : WeakSet[Callable[[Tuple[StdFd, str]], Awaitable[None]]]
    
    loop : asyncio.AbstractEventLoop
    live : bool
    
    
    
    def __init__(self, *, 
        manager : ModelManager = TfModelManager(),
        latency : float = 0.1,
        app : FastAPI = FastAPI()
    ) -> None:
        
        self.manager = manager
        self.app = app
        
        self.latency = latency
        
        self.action_buff_lock = asyncio.Lock()
        self.action_buff = Queue()
        
        self.out_buff_lock = asyncio.Lock()
        self.out_buff = Queue()
        
        self.out_cbs_lock = asyncio.Lock()
        self.out_cbs = WeakSet()
        
        self.loop = asyncio.get_event_loop()
        self.live = True
        
    async def push_action(self, action : Queue[Callable[[], AsyncIterator[Tuple[StdFd, str]]]]):
        await self.action_buff_lock.acquire()
        self.action_buff.put(action)
        self.action_buff_lock.release()
        
    
    async def subscribe_out_buff(self, cb : Callable[[Tuple[StdFd, str]], Awaitable[None]]):
        await self.out_cbs_lock.acquire()
        self.out_cbs.add(cb)
        self.out_cbs_lock.release()
    
    async def unsubscribe_out_buff(self, cb : Callable[[Tuple[StdFd, str]], Awaitable[None]]):
        await self.out_cbs_lock.acquire()
        self.out_cbs.remove(cb)
        self.out_cbs_lock.release()
        
    def build_app(self)->None:
        
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @self.app.get("/_health")
        async def check_health():
            return True
        
        @self.app.websocket("/apply")
        async def stream_apply(websocket : WebSocket):
            
            await websocket.accept()
            
            # wait for apply payload
            
            try:
                config = ModelConfig.parse_obj(
                    json.loads(await websocket.receive_text())
                )
            except Exception as e:
                print(e)
                await websocket.close()
                return
            
            # subscribe to the buffer
            async def send_apply_to_client(data : Tuple[StdFd, str]):
                if data[0] == StdFd.stdeof:
                    await websocket.close()
                    return
                try:
                    await websocket.send_json(data)
                except (WebSocketDisconnect, Exception) as e:
                    print(e)  
            await self.subscribe_out_buff(send_apply_to_client)
            
            # push your action buff
            async def apply():
                async for res in self.manager.apply(config=config):
                    yield res
            await self.push_action(apply)
            
            try:
                while True:
                    await websocket.receive()
            except (WebSocketDisconnect, Exception) as e:
                await self.unsubscribe_out_buff(send_apply_to_client)
                
        @self.app.websocket("/destroy")
        async def stream_destroy(websocket : WebSocket):
            
            await websocket.accept()
            
            # subscribe to the buffer
            async def send_destroy_to_client(data : Tuple[StdFd, str]):
                
                if data[0] == StdFd.stdeof:
                    await websocket.close()
                    return
                
                try:
                    await websocket.send_json(data)
                except (WebSocketDisconnect, Exception) as e:
                    print(e)  
            await self.subscribe_out_buff(send_destroy_to_client)
            
            # push your action buff
            async def destroy():
               async for res in self.manager.destroy():
                   yield res
            await self.push_action(destroy)
            
            try:
                while True:
                    await websocket.receive()
            except (WebSocketDisconnect, Exception) as e:
                await self.unsubscribe_out_buff(send_destroy_to_client)
                
        @self.app.websocket("/observe")
        async def stream_observe(websocket : WebSocket):
            
            await websocket.accept()
            
            # subscribe to the buffer
            async def send_observe_to_client(data : Tuple[StdFd, str]):
                try:
                    await websocket.send_json(data)
                except (WebSocketDisconnect, Exception) as e:
                    print(e)  
            await self.subscribe_out_buff(send_observe_to_client)
            
            try:
                while True:
                    await websocket.receive()
            except (WebSocketDisconnect, Exception) as e:
                await self.unsubscribe_out_buff(send_observe_to_client)
                
        @self.app.get("/model_url")
        async def get_model_url():
          res = await self.manager.get_url()
          return res
                
    
    async def run_manager(self):
        """Runs the manager
        """

        while self.live:
        
            try:
                
                # await self.action_buff_lock.acquire()
                action = self.action_buff.get(block=False)
                # self.action_buff_lock.release()
                
                async for fd, res in action():
                    await asyncio.gather(
                        *[cb((int(fd), res)) for cb in self.out_cbs]
                    )
                    
                
            except Empty:
                await asyncio.sleep(self.latency)      
         
    async def run_server(self, *, host : str = "0.0.0.0", port : int = 8000):
       uvicorn.run(app=self.app, host=host, port=port)
        
    def kill(self):
        self.live = False
        self.loop.stop()
        self.loop.close()
    
    def serve(self, *,  host : Optional[str] = "0.0.0.0", port : Optional[int] = 8000) -> None:
        self.build_app()
        self.loop.add_signal_handler(SIGINT, lambda : self.kill)
        self.loop.add_signal_handler(SIGTERM, lambda : self.kill)
        self.loop.run_until_complete(asyncio.gather(
            self.run_manager(),
            self.run_server(host=host,port=port)
        ))