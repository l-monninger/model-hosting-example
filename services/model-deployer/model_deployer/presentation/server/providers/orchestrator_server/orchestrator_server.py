from ...server import Server
from typing import Optional
import uvicorn
from fastapi import FastAPI 
from model_deployer.logic.orchestrator import Orchestrator
from model_deployer.logic.orchestrator.providers.deployer_registry_orchestrator import DeployerRegistryOrchestrator
import asyncio
import nest_asyncio
nest_asyncio.apply()
from signal import SIGINT, SIGTERM
from model_deployer.util.model_config import ModelStartConfig, ModelIdConfig
from fastapi.middleware.cors import CORSMiddleware

class OrchestratorServer(Server):
    
    app : FastAPI
    orchestrator : Orchestrator
    loop : asyncio.AbstractEventLoop
    
    def __init__(
        self,
        *, app : FastAPI = FastAPI(),
        orchestrator : Orchestrator = DeployerRegistryOrchestrator(),
        loop : asyncio.AbstractEventLoop = asyncio.get_event_loop()
    ) -> None:
        self.app = app
        self.orchestrator = orchestrator
        self.loop = loop
    
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
        
        @self.app.post("/start_model")
        async def start_model(start : ModelStartConfig)->str:
            return await self.orchestrator.start_model(id=start.id, prompt=start.prompt)
        
        @self.app.post("/halt_model")
        async def halt_model(halt : ModelIdConfig)->str:
            return await self.orchestrator.halt_model(id=halt.id)
        
        @self.app.post("/destory_model")
        async def halt_model(destroy : ModelIdConfig)->str:
            return await self.orchestrator.halt_model(id=destroy.id)
        
        @self.app.get("/sidecar_url/{id}")
        async def get_sidecar_url(id : str):
            return await self.orchestrator.get_sidecar_url(id=id)
        
        @self.app.get("/model_url/{id}")
        async def get_model_url(id : str):
            return await self.orchestrator.get_model_url(id=id)
        

         
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
            self.run_server(host=host,port=port)
        ))