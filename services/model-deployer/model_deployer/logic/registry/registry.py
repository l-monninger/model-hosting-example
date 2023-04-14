from typing import Protocol

class Registry(Protocol):
    
    async def next_id(self)->str:
        pass
    
    async def set_sidecar_url(self, url : str)->str:
        pass
    
    async def set_latent_model_url(self, url : str)->str:
        pass