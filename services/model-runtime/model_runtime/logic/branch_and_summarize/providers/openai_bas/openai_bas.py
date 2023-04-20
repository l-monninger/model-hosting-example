from model_runtime.logic.branch_and_summarize.branch_and_summarize import BranchAndSummarize
from typing import Iterable, List, AsyncIterator
from .brancher import Brancher
from .summarizer import Summarizer
from asyncio import sleep, Lock


class OpenAiBaS(BranchAndSummarize[str, str, str]):
    
    prompts : List[str]
    size : int
    
    branches : List[str]
    new_branches : bool
    
    summary : str
    new_summary : bool
    
    latency : int
    stream_latency : int
    lock : Lock
    
    def __init__(self, *, size : int = 10, latency : int = 5, stream_latency : int = 1) -> None:
        self.prompts = []
        self.size = size
        self.branches = []
        self.summary = ""
        self.latency = latency
        self.stream_latency = stream_latency
        self.lock = Lock()
        self.new_branches = False
        self.new_summary = False
        
    async def prompt(self, prompt: str):
        return self.prompts.append(prompt)
    
    async def branch(self) -> List[str]:
        
        brancher = Brancher(branches=self.size, prompts=self.prompts)
        new_branches = await brancher.branch(self.summary)
        
        await self.lock.acquire()
        self.branches = new_branches
        self.new_branches = True
        self.lock.release()
        
        await sleep(self.latency) # introduce latency here
        return self.branches
    
    async def summarize(self) -> str:
        
        summarizer = Summarizer(prompts=self.prompts)
        new_summary = await summarizer.summarize(self.branches)
        
        await self.lock.acquire()
        self.summary = new_summary
        self.new_summary = True
        self.lock.release()
        
        return self.summary
    
    async def get_prompt(self) -> str:
        
        while True:
            if len(self.prompts) > 0:
                return self.prompts[-1]
            await sleep(self.latency)
    
    async def get_branches(self) -> List[str]:
        return self.branches
    
    async def get_branch_stream(self) -> AsyncIterator[List[str]]:
        
        while True:
            while not self.new_branches:
                await sleep(self.stream_latency)
                
            await self.lock.acquire()
            self.new_branches = False
            yield self.branches
            self.lock.release()
    
    async def get_summary(self) -> str:
        return self.summary
    
    async def get_summary_stream(self) -> AsyncIterator[str]:
        
        while True:
            while not self.new_summary:
                await sleep(self.stream_latency)
                
            await self.lock.acquire()
            self.new_summary = False
            yield self.summary
            self.lock.release()