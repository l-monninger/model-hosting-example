from typing import Protocol, TypeVar, Generic, Iterable, AsyncIterator

Branch = TypeVar("Branch")
Summary = TypeVar("Summary")
Prompt = TypeVar("Prompt")

class BranchAndSummarize(Protocol, Generic[Branch, Summary, Prompt]):
    
    async def prompt(self, prompt : Prompt):
        pass
    
    async def branch(self)->Iterable[Branch]:
        pass
    
    async def summarize(self)->Summary:
        pass
    
    async def get_prompt(self)->Prompt:
        pass
    
    async def get_branches(self)->Iterable[Branch]:
        pass
    
    async def get_branch_stream(self)->AsyncIterator[Iterable[Branch]]:
        pass
    
    async def get_summary(self)->Summary:
        pass
    
    async def get_summary_stream(self)->AsyncIterator[Summary]:
        pass
    
    async def run(self):
        
        # wait until a prompt is available
        await self.get_prompt()
        
        while True:
            await self.branch()
            await self.summarize()