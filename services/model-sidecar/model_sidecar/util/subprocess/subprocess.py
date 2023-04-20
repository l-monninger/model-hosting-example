import os
import subprocess
from threading import Thread
from queue import Queue
from typing import IO, AsyncIterator, Dict, Iterable, Optional, Tuple
from enum import Enum, IntEnum
import sys


class StdFd(IntEnum):
    stdout = 0
    stderr = 1
    stdeof = 2

def read_fd(pipe :  IO[bytes], queue : Queue[Tuple[StdFd, bytes]], fd : Optional[StdFd] = StdFd.stdout):
    try:
        with pipe:
            for line in iter(pipe.readline, b''):
                queue.put((fd, line))
    finally:
        queue.put((StdFd.stdeof, bytes("", encoding="UTF-8")))

async def call_with_env(cmd : Iterable[str], *, env : Dict[str, str])->AsyncIterator[Tuple[StdFd, bytes]]:
    
    print(cmd)
    queue : Queue[Tuple[StdFd, bytes]] = Queue()
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        env=env,
    )
   
    Thread(target=read_fd, args=[process.stdout, queue, StdFd.stdout]).start()
    Thread(target=read_fd, args=[process.stderr, queue, StdFd.stderr]).start()
    
    hits = 0
    while hits < 2:
        try:
            next = queue.get(block=False)
            
            if next[0] == StdFd.stdeof:
                hits += 1
                continue
        
            yield next
        except Exception:
            continue
        
    yield (StdFd.stdeof, bytes("", encoding="UTF-8"))