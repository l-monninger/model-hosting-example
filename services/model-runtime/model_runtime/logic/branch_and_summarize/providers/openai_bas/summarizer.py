import openai
from typing import List, Dict
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Summarizer:
    
    size : int = 1024
    model_engine : str = "gpt-3.5-turbo"
    sys_prompt_template : str = f"""
You are a brainstorming assistant. You will interact with a User and Brancher.

The User will ask for help generating ideas and solutions to problems.

The Brancher will suggest multiple solutions to the user's prompts.

You will summarize these solutions, judge them, and present your findings as a follow-up question for the Brancher.

Keep your responses short.
"""
    prompts : List[str]
    
    def __init__(self, *, prompts : List[str] = []) -> None:
        self.prompts = prompts
    
    def get_sys_prompt_message(self)->Dict[str, str]:
        return {
            "role" : "system",
            "content" : self.sys_prompt_template
        }
        
    def get_prompt_messages(self)->List[Dict[str, str]]:
        return [
            {
                "role" : "user",
                "content" : "User: " + prompt
            }
            for prompt in self.prompts
        ]
        
    def make_brancher_message(self, prompt : str)->Dict[str, str]:
        return {
            "role" : "user",
            "content" : "Brancher: " + prompt
        }

    async def summarize(self, branches : List[str])->str:
        
        completion = await openai.ChatCompletion.acreate(
            max_tokens=self.size,
            messages=[
                self.get_sys_prompt_message(),
                *self.get_prompt_messages(),
                *[
                    self.make_brancher_message(prompt)
                    for prompt in branches
                ]
            ],
            model=self.model_engine,
            # frequency_penalty=0,
        )
        
        response : str = completion["choices"][0]["message"]["content"]
        return response