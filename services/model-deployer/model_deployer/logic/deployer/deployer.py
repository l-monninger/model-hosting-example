from typing import Protocol, Optional, AsyncIterator, Tuple

class Deployer(Protocol):
    
    
    # we're going to use the google cloud API instead of terraform
    # so this might be different 
    async def deploy_sidecar(self, id : str)->str:
        """Deploys a side car and returns its url.

        Args:
            id (str): _description_

        Returns:
            str: _description_
        """
        pass
    
    async def destroy_sidecar(self, id : str):
        """Destroys a side

        Args:
            id (str): _description_
        """
        pass
