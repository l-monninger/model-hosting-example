from ...server import Server
from model_runtime.logic.branch_and_summarize import BranchAndSummarize
from model_runtime.logic.branch_and_summarize.providers.openai_bas import OpenAiBaS
from model_runtime.util.model_prompt.model_promp import ModelPrompt
from fastapi import FastAPI, WebSocketDisconnect, WebSocket
import uvicorn
import nest_asyncio
from weakref import WeakSet
from typing import Callable, Awaitable, Iterable, Optional, List
import asyncio
nest_asyncio.apply()
from fastapi.middleware.cors import CORSMiddleware

class BasServer(Server):
    
    bas : BranchAndSummarize[str, str, str]
    app : FastAPI
    
    cached_branches_lock : asyncio.Lock
    cached_branches : List[str]
    
    branches_cbs_lock : asyncio.Lock
    branches_cbs : WeakSet[Callable[[Iterable[str]], Awaitable[None]]]
    
    cached_summary_lock : asyncio.Lock
    cached_summary : str
    
    summary_cbs_lock : asyncio.Lock
    summary_cbs : WeakSet[Callable[[str], Awaitable[None]]]
    
    loop : asyncio.AbstractEventLoop
    
    
    def __init__(self, *, 
        bas : BranchAndSummarize[str,str,str] = OpenAiBaS(size=7, latency=10),
        app : FastAPI = FastAPI()
    ) -> None:
        self.bas = bas
        self.app = app
        
        self.branches_cbs_lock = asyncio.Lock()
        self.branches_cbs = WeakSet()
        
        self.summary_cbs_lock = asyncio.Lock()
        self.summary_cbs = WeakSet()
        
        self.loop = asyncio.get_event_loop()
        
        self.cached_branches_lock = asyncio.Lock()
        self.cached_branches = []
        
        self.cached_summary_lock = asyncio.Lock()
        self.cached_summary = ""
        
    async def subscribe_branches(self, cb : Callable[[Iterable[str]], Awaitable[None]]):
        await self.branches_cbs_lock.acquire()
        self.branches_cbs.add(cb)
        self.branches_cbs_lock.release()
    
    async def unsubscribe_branches(self, cb : Callable[[Iterable[str]], Awaitable[None]]):
        await self.branches_cbs_lock.acquire()
        self.branches_cbs.remove(cb)
        self.branches_cbs_lock.release()
    
    async def subscribe_summary(self, cb : Callable[[str], Awaitable[None]]):
        await self.summary_cbs_lock.acquire()
        self.summary_cbs.add(cb)
        self.summary_cbs_lock.release()
    
    async def unsubscribe_summary(self, cb : Callable[[str], Awaitable[None]]):
        await self.summary_cbs_lock.acquire()
        self.summary_cbs.remove(cb)
        self.summary_cbs_lock.release()
        
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
        
        @self.app.post("/prompt")
        async def prompt(prompt : ModelPrompt):
            await self.bas.prompt(prompt=prompt.prompt)
        
        @self.app.websocket("/branches")
        async def stream_branches(websocket : WebSocket):
            await websocket.accept()
            
            async def send_to_client(branches : Iterable[str]):
                try:
                    await websocket.send_json(branches)
                except (WebSocketDisconnect, Exception) as e:
                    print(e)
                
            await self.subscribe_branches(send_to_client)
            
            await websocket.send_json(self.cached_branches)
            
            try:
                while True:
                    await websocket.receive()
            except (WebSocketDisconnect, Exception) as e:
                await self.unsubscribe_summary(send_to_client)
                
        @self.app.websocket("/summary")
        async def stream_summaries(websocket : WebSocket):
            await websocket.accept()
            
            async def send_to_client(summary : str):
                try:
                    await websocket.send_json(summary)
                except (WebSocketDisconnect, Exception) as e:
                    print(e)
                
            await self.subscribe_summary(send_to_client)
            
            await websocket.send_json(self.cached_summary)
            
            try:
                while True:
                    await websocket.receive()
            except (WebSocketDisconnect, Exception) as e:
                await self.unsubscribe_summary(send_to_client)
                
        
    async def stream_branches(self):
        
        async for branches in self.bas.get_branch_stream():
            await self.cached_branches_lock.acquire()
            self.cached_branches = branches
            self.cached_branches_lock.release()
            await self.branches_cbs_lock.acquire()
            await asyncio.gather(
                *[cb(branches) for cb in self.branches_cbs]
            )
            self.branches_cbs_lock.release()
                
    
    async def stream_summary(self):
    
        async for summary in self.bas.get_summary_stream():
            await self.cached_summary_lock.acquire()
            self.cached_summary = summary
            self.cached_summary_lock.release()
            await self.summary_cbs_lock.acquire()
            await asyncio.gather(
                *[cb(summary) for cb in self.summary_cbs]
            )
            self.summary_cbs_lock.release()
    
    async def run_bas(self):
        await asyncio.gather(
            self.stream_branches(),
            self.stream_summary(),
            self.bas.run()
        )
         
    async def run_server(self, *, host : str = "0.0.0.0", port : int = 8000):
       uvicorn.run(app=self.app, host=host, port=port)
        
    
    def serve(self, *,  host : Optional[str] = "0.0.0.0", port : Optional[int] = 8000) -> None:
        self.build_app()
        self.loop.run_until_complete(asyncio.gather(
            self.run_bas(),
            self.run_server(host=host,port=port)
        ))