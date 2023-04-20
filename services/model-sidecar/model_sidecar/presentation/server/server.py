from typing import Protocol, Optional

class Server(Protocol):
    
    def serve(self, *, host : Optional[str] = None, port : Optional[int] = None):
        pass
    
    def kill(self):
        pass