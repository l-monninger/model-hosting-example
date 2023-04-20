import unittest
from model_sidecar.util.runtime.deasync import deasync
from .tf_model_manager import TfModelManager, ModelConfig

class TestTfModelManager(unittest.TestCase):
    
    
    @deasync
    async def test_apply(self):
        
        mm = TfModelManager()
        async for line in mm.apply(ModelConfig(
            id="abcdefg",
            width=1,
            depth=2,
            latency=3,
            prompt=""
        )):
            print(line)
            
    @deasync
    async def test_destroy(self):
        
        mm = TfModelManager()
        async for line in mm.destroy():
            print(line)