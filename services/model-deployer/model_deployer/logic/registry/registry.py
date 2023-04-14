from typing import Protocol

class Registry(Protocol):
    
    async def next_id(self)->str:
        pass
    
    async def set_sidecar_url(self, *, id : str, url : str)->str:
        pass
    
    async def get_sidecar_url(self, *, id : str)->str:
        pass
    
    async def remove_sidecar_url(self, *, id : str)->str:
        pass
    
    async def set_latent_model_url(self, *, id : str, url : str)->str:
        pass
    
    async def get_latent_model_url(self, *, id : str)->str:
        pass
    
    async def remove_latent_model_url(self, *, id : str)->str:
        pass
    