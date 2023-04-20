from pydantic import BaseModel
from typing import Optional

class ModelIdConfig(BaseModel):
    id : Optional[str]

class ModelStartConfig(ModelIdConfig):
    prompt : Optional[str]
    