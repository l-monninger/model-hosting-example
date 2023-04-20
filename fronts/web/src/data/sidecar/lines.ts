import React, { useEffect, useReducer, useState } from "react";
import { SidecarLine, ModelConfig } from "../../util";

export const getSidecarObserverConnection = (url : string)=>{
    return new WebSocket(`${url}/observe`)
}

export const getSidecarApplyConnection = (url : string)=>{
    return new WebSocket(`${url}/apply`)
}

export const getSidecarDestroyConnection = (url : string)=>{
    return new WebSocket(`${url}/destroy`)
}

export const useSidecarObserverLines = (url : string, size : number = 1024) : SidecarLine[] =>{

    const _url = url.replace("http", "ws");
    const [needsSocket, setNeedsSocket] = useState(true);
    const [lines, addSidecarLine] = useReducer((oldSidecarLines : SidecarLine[], line : SidecarLine) : SidecarLine[]=>{
        const _lines = oldSidecarLines.slice(0, size-1);
        return [
            line,
            ..._lines
        ]

    }, [])

    useEffect(()=>{

        let timeout : number | undefined = undefined;
        
        if(needsSocket){

            let ws = getSidecarObserverConnection(_url)
            ws.onmessage = (msg)=>{
                
                addSidecarLine(JSON.parse(msg.data) as SidecarLine)
            }
            ws.onclose = ()=>{
                
                timeout = setTimeout(()=>{
                    setNeedsSocket(true)
                }, 500);
                
            }   
    
            setNeedsSocket(false)
        }

        return ()=>{
            if(timeout) clearTimeout(timeout);
        }

    }, [needsSocket])

    return lines
}

export const useSidecarApply = (url : string, size : number = 1024) : [
    SidecarLine[],
    ((config : ModelConfig)=>Promise<void>)
] =>{

    const _url = url.replace("http", "ws");
    const [needsSocket, setNeedsSocket] = useState(false);
    const [lines, addSidecarLine] = useReducer((oldSidecarLines : SidecarLine[], line : SidecarLine) : SidecarLine[]=>{
        const _lines = oldSidecarLines.slice(0, size-1);
        return [
            line,
            ..._lines
        ]

    }, [])
    const [apply, setApply] = useState<(config : ModelConfig)=>Promise<void>>(async ()=>{
        setNeedsSocket(true)
    });

    useEffect(()=>{

        let timeout : number | undefined = undefined;
        
        if(needsSocket){

            let ws = getSidecarApplyConnection(_url)

            ws.onopen = ()=>{
                setApply(async (config : ModelConfig)=>{
                    ws.send(JSON.stringify(config))
                })
            }

            ws.onmessage = (msg)=>{
                
                addSidecarLine(JSON.parse(msg.data) as SidecarLine)
            }
            ws.onclose = ()=>{
                
                timeout = setTimeout(()=>{
                    setNeedsSocket(false);
                    setApply(async ()=>{
                        setNeedsSocket(true)
                    })
                }, 100);

            }   
    
            setNeedsSocket(false)
        }

        return ()=>{
            if(timeout) clearTimeout(timeout);
        }

    }, [needsSocket])

    return [lines, apply];
}

export const useSidecarDestroy = (url : string, size : number = 1024) : [
    SidecarLine[],
    ((config : ModelConfig)=>Promise<void>)
] =>{

    const _url = url.replace("http", "ws");
    const [needsSocket, setNeedsSocket] = useState(false);
    const [lines, addSidecarLine] = useReducer((oldSidecarLines : SidecarLine[], line : SidecarLine) : SidecarLine[]=>{
        const _lines = oldSidecarLines.slice(0, size-1);
        return [
            line,
            ..._lines
        ]

    }, [])
    const [apply, setApply] = useState<(config : ModelConfig)=>Promise<void>>(async ()=>{
        setNeedsSocket(true)
    });

    useEffect(()=>{

        let timeout : number | undefined = undefined;
        
        if(needsSocket){

            let ws = getSidecarDestroyConnection(_url)

            ws.onopen = ()=>{
           
            }

            ws.onmessage = (msg)=>{
                
                addSidecarLine(JSON.parse(msg.data) as SidecarLine)
            }
            ws.onclose = ()=>{
                
                timeout = setTimeout(()=>{
                    setNeedsSocket(false);
                    setApply(async ()=>{
                        setNeedsSocket(true)
                    })
                }, 100);

            }   
    
            setNeedsSocket(false)
        }

        return ()=>{
            if(timeout) clearTimeout(timeout);
        }

    }, [needsSocket])

    return [lines, apply];
}