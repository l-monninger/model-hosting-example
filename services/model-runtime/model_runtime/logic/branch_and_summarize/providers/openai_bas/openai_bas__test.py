import unittest
from model_runtime.util.runtime.deasync import deasync
from .openai_bas import OpenAiBaS
from asyncio import create_task

class TestOpenAiBas(unittest.TestCase):
    
    @deasync
    async def test_runs(self):
        bas = OpenAiBaS()
        await bas.prompt("Find me the best Milkshake in Palo Alto.")
        await bas.run()
        
    @deasync
    async def test_summary_streams(self):
        bas = OpenAiBaS()
        await bas.prompt("Find me the best Milkshake in Palo Alto.")
        task = create_task(bas.run())
        
        i = 0
        async for summary in bas.get_summary_stream():
            self.assertIsNotNone(summary)
            i+=1
            if i > 3:
                break
            
        task.cancel()
            
    @deasync
    async def test_branches_streams(self):
        bas = OpenAiBaS()
        await bas.prompt("Find me the best Milkshake in Palo Alto.")
        task = create_task(bas.run())
        
        i = 0
        async for branches in bas.get_branch_stream():
            self.assertIsNotNone(len(branches) == 10)
            i+=1
            if i > 3:
                break
        
        task.cancel()