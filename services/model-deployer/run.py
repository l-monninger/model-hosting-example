from model_deployer import OrchestratorServer
import os
import nest_asyncio
nest_asyncio.apply()
import asyncio

if __name__ == "__main__":
    
    server = OrchestratorServer()
    loop = asyncio.get_event_loop()
    env_prompt = os.environ.get("PROMPT", None)
    server.serve(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

   
