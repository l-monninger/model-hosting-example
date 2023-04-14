from typing import Protocol, Optional, Tuple, AsyncIterator

"""
0 will be used for stderror
1 will be used for stdout
2 will be used for the id
3 will be used for the sidecar url
4 will be used for the model url
"""

class Orchestrator(Protocol):
    
    async def start_model(self, *, id : Optional[str] = None, prompt : Optional[str] = None)->str:
        pass
    
    async def halt_model(self, *, id : str)->str:
        pass
    
    async def destroy_model(self, *, id : str)->str:
        pass
    
    async def get_sidecar_url(self, *, id : str)->str:
        pass
    
    async def get_model_url(self, *, id : str)->str:
        pass