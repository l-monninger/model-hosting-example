import openai
from typing import List, Dict
from dotenv import load_dotenv
import os
import json
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Brancher:
    
    size : int = 512
    model_engine : str = "gpt-3.5-turbo"
    delimiter : str = "[[[[<break>]]]]"
    branches : int 
    sys_prompt_template : str = f"""
You are a helpful brainstorming assistant. You will interact with a User and Summarizer. You output JSON arrays.

You will develop <num> solutions to the User's prompts. The Summarizer will help you by providing feedback and updated prompts of its own which you must also address.

Always output your <num> different solutions as a JSON array.

Example JSON array output format:
[
    "<solution text 1>",
    // ...,
    "<solution text <num>>"
]
"""
    prompts : List[str]
    
    def __init__(self, *, prompts : List[str] = [], branches : int = 10) -> None:
        self.prompts = prompts
        self.branches = branches
    
    def get_sys_prompt_message(self)->Dict[str, str]:
        return {
            "role" : "system",
            "content" : self.sys_prompt_template.replace("<num>", str(self.branches))
        }
        
    def get_prompt_messages(self)->List[Dict[str, str]]:
        return [
            {
                "role" : "user",
                "content" : "User: " + prompt + "\nPlease respond with a JSON array."
            } for prompt in self.prompts
        ]
        
    def make_summarizer_message(self, prompt : str)->Dict[str, str]:
        return {
            "role" : "user",
            "content" : "Summarizer: " + prompt + "\nPlease respond with a JSON array."
        }

    async def branch(self, text : str)->List[str]:
        completion = await openai.ChatCompletion.acreate(
            max_tokens=self.size,
            messages=[
                self.get_sys_prompt_message(),
                *self.get_prompt_messages(),
                self.make_summarizer_message(text)
            ],
            model=self.model_engine,
            # frequency_penalty=0,
        )
        
        response : str = completion["choices"][0]["message"]["content"]
        try:
            l = json.loads(response)
            return l
        except Exception:
            return [response]