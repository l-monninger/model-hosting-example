from ...orchestrator import Orchestrator
from typing import Optional, AsyncIterator, Tuple 
from model_deployer.logic.deployer import Deployer
from model_deployer.logic.deployer.providers.cloud_run_deployer import CloudRunDeployer
from model_deployer.logic.registry import Registry
from model_deployer.logic.registry.providers.redis_registry import RedisRegistry

import aiohttp
from websockets import client
from fastapi import HTTPException

class DeployerRegistryOrchestrator(Orchestrator):
    
    deployer : Deployer
    registry : Registry
    
    def __init__(
        self, *, 
        deployer : Deployer = CloudRunDeployer(),
        registry : Registry = RedisRegistry()
    ) -> None:
        self.deployer = deployer
        self.registry = registry
    
    async def get_sidecar_url(self, *, id: str) -> str:
        return await self.registry.get_sidecar_url(id)
    
    async def get_model_url_at_sidecar(self, *, id: str) -> str:
        
        sidecar_url = await self.get_sidecar_url(id=id)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{sidecar_url}/model_url") as response:
                return await response.text()

    
    async def get_model_url(self, *, id: str) -> str:
        
        url_at_sidecar = await self.get_model_url_at_sidecar(id=id)
        self.registry.set_latent_model_url(id=id, url=url_at_sidecar)
        return url_at_sidecar
    
    async def create_model(self, *, prompt: Optional[str] = None) -> str:
        
        # start the sidecar
        id = await self.registry.next_id()
        sidecar_url = await self.deployer.deploy_sidecar(id)
        await self.registry.set_sidecar_url(id, sidecar_url)
        return sidecar_url
        
        
    
    async def start_model(self, *, id: Optional[str] = None, prompt: Optional[str] = None) -> str:
        
        if id == None:
            return await self.create_model(prompt=prompt)
        else:
            return await self.get_sidecar_url(id=id)
        
    async def destroy_model(self, *, id: str) -> str:
        """Use for top-down destroys.

        Args:
            id (str): _description_

        Returns:
            str: _description_
        """
        # halt (destroy) the model
        await self.halt_model(id)
        
        # destroy the sidecar
        sidecar_url = await self.get_sidecar_url(id=id)
        await self.deployer.destroy_sidecar(id)    
        await self.registry.remove_sidecar_url(id)
        
        return sidecar_url
    
    async def halt_model(self, *, id: str) -> str:
        # destroy the model
        model_url = await self.get_model_url(id=id)
        sidecar_url = await self.get_sidecar_url(id=id)
        stream = client.connect(f"{sidecar_url}/destroy")
        async for fd, line in stream:
            if fd == 0:
                raise HTTPException(500, detail=f"Destruction of model failed on: {line}")
        await self.registry.remove_latent_model_url(id)
        
        return model_url