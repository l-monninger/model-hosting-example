from pydantic import BaseModel
from typing import Optional

class ModelConfig(BaseModel):
    
    width : Optional[str]
    depth : Optional[str]
    latency : Optional[str]
    prompt : Optional[str]