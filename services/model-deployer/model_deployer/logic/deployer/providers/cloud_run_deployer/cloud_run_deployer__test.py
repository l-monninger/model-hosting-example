import unittest
from model_deployer.util.runtime.deasync import deasync
from .cloud_run_deployer import CloudRunDeployer
import requests as re
import asyncio

class TestCloudRunDeployer(unittest.TestCase):
    
    @deasync
    async def test_creates_and_destroys(self):
        
        id = "testdeployer0x01"
        deployer = CloudRunDeployer()
        url = await deployer.deploy_sidecar(id)
        res = re.get(url).json()
        self.assertEquals(res, {'detail': 'Not Found'})
        await deployer.destroy_sidecar(id)
        await asyncio.sleep(4)
        self.assertRaises(Exception, lambda : re.get(url).json())
        