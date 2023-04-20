from typing import Protocol, TypeVar, Generic, AsyncIterator, Tuple
from model_sidecar.util.subprocess import StdFd

Config = TypeVar("Config")

class ModelManager(Protocol, Generic[Config]):
    
    
    async def apply(self, config : Config)->AsyncIterator[Tuple[StdFd, str]]:
        pass
    
    async def destroy(self)->AsyncIterator[Tuple[StdFd, str]]:
        pass
    
    async def get_url(self)->str:
        pass