from model_sidecar import ModelManagerServer
import os
import nest_asyncio
nest_asyncio.apply()
import asyncio

if __name__ == "__main__":
    
    try:
        server = ModelManagerServer()
        loop = asyncio.get_event_loop()
        env_prompt = os.environ.get("PROMPT", None)
        if env_prompt is not None:
            loop.run_until_complete(server.bas.prompt(env_prompt))
        server.serve(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    except KeyboardInterrupt:
        pass
    finally:
        exit()
