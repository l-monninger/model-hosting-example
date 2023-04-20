from ...registry import Registry
import redis
import os

class RedisRegistry(Registry):
    
    store : redis.Redis
    root : str = "MODEL_DEPLOYER"
    delimiter : str = "::,::"
    sidecar_urls : str = "sidecars"
    latent_model_urls : str = "models"
    encoding : str = "UTF-8"
    
    def __init__(
        self,
        *,
        store = redis.Redis(
            host=os.environ.get("REDIS_HOST", "0.0.0.0"), 
            port=os.environ.get("REDIS_PORT", 6379), 
            db=0
        )
    ) -> None:
        self.store = store
        
    async def next_id(self) -> str:
        return str(self.store.incr(self.root))
    
    async def set_sidecar_url(self, *, id: str, url: str) -> str:
        path = f"{self.root}{self.delimiter}{self.sidecar_urls}{self.delimiter}{id}"
        self.store.set(
            path,
            url
        )
        return await self.get_sidecar_url(id=id)
    
    async def get_sidecar_url(self, *, id: str) -> str:
        path = f"{self.root}{self.delimiter}{self.sidecar_urls}{self.delimiter}{id}"
        return str(self.store.get(path), encoding=self.encoding)
    
    async def remove_sidecar_url(self, *, id: str) -> str:
        path = f"{self.root}{self.delimiter}{self.sidecar_urls}{self.delimiter}{id}"
        return self.store.delete(path)
    
    async def set_latent_model_url(self, *, id: str, url: str) -> str:
        path = f"{self.root}{self.delimiter}{self.latent_model_urls}{self.delimiter}{id}"
        self.store.set(
            path,
            url
        )
        return await self.get_latent_model_url(id=id)
    
    async def get_latent_model_url(self, *, id: str) -> str:
        path = f"{self.root}{self.delimiter}{self.latent_model_urls}{self.delimiter}{id}"
        return str(self.store.get(path), encoding=self.encoding)
    
    async def remove_latent_model_url(self, *, id: str) -> str:
        path = f"{self.root}{self.delimiter}{self.latent_model_urls}{self.delimiter}{id}"
        return self.store.delete(path)