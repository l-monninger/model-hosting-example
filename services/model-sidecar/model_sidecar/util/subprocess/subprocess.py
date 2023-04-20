import os
import subprocess
from threading import Thread
from queue import Queue, Empty
from typing import IO, AsyncIterator, Dict, Iterable, Optional, Tuple
from enum import Enum, IntEnum
import sys
import asyncio


class StdFd(IntEnum):
    stdout = 0
    stderr = 1
    stdeof = 2

async def read_fd(pipe :  asyncio.StreamReader, queue : Queue[Tuple[StdFd, bytes]], fd : Optional[StdFd] = StdFd.stdout):
    try:
        while line := await pipe.readline():
            queue.put((fd, line))
    finally:
        queue.put((StdFd.stdeof, bytes("", encoding="UTF-8")))

async def call_without_env(cmd : Iterable[str])->AsyncIterator[Tuple[StdFd, bytes]]:
    
    queue : Queue[Tuple[StdFd, bytes]] = Queue()
    
    sys.stdin.flush()
    sys.stdout.flush()
    sys.stderr.flush()
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE, 
        stderr=asyncio.subprocess.PIPE, 
        # env=env,
        stdin=open(os.devnull)
    )
    
    tout = asyncio.create_task(read_fd(process.stdout, queue, StdFd.stdout))
    terr = asyncio.create_task(read_fd(process.stderr, queue, StdFd.stderr))
    
    hits = 0
    while hits < 2:
        try:
            next = queue.get(block=False)
            
            if next[0] == StdFd.stdeof:
                hits += 1
                continue
        
            yield next
        except Empty:
            await asyncio.sleep(0)
            continue
        
    yield (StdFd.stdeof, bytes("", encoding="UTF-8"))
    
    tout.cancel()
    terr.cancel()
    
    