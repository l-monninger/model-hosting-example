from ...model_manager import ModelManager
from model_sidecar.util.model_config import ModelConfig
from typing import IO, AsyncIterator, Dict, Iterable, Optional
import os
from model_sidecar.util.subprocess import call_without_env, StdFd
from typing import Tuple
import re
from dotenv import load_dotenv
load_dotenv()

GKR_CONTAINER_REG = os.environ.get("TF_VAR_model_runtime_container", "gcr.io/blog-model-hosting/model-runtime")


class TfModelManager(ModelManager[ModelConfig]):
    
    encoding : str = "UTF-8"
    url : Optional[str] 
    
    def __init__(self) -> None:
        super().__init__()
        self.url = None
        
    
    async def apply(self, config: ModelConfig)->AsyncIterator[Tuple[StdFd, str]]:
        
        env = {
            **os.environ, 
            'PATH': '/usr/sbin:/sbin:/usr/bin:/bin' + os.environ['PATH'],
            "TF_VAR_model_runtime_container" : GKR_CONTAINER_REG,
            "TF_VAR_model_runtime_prompt" : config.prompt
        }

        
        async for fd, line in call_without_env([
            "terraform", "apply", "-auto-approve", 
            f"-var=model_runtime_container={GKR_CONTAINER_REG}",
            f"-var=model_runtime_prompt={config.prompt}"
        ]):
            str_line = str(line, encoding="UTF-8")
            match = re.search("cloud_run_instance_url = \"(https://.*?)\"", str_line)
            if match is not None:
                self.url = match.group(1)
        
            yield (fd, str_line)
    
    async def destroy(self)->AsyncIterator[Tuple[StdFd, str]]:
        
        env = {
            **os.environ, 
            'PATH': '/usr/sbin:/sbin:' + os.environ['PATH'],
            "TF_VAR_model_runtime_container" : GKR_CONTAINER_REG
        }
        
        async for fd, line in call_without_env([
            "terraform", "destroy", "-auto-approve",
            f"-var=model_runtime_container={GKR_CONTAINER_REG}",
        ]):
            yield (fd, str(line, encoding="UTF-8"))
            
        self.url = None
            
    async def get_url(self) -> str:
        return self.url