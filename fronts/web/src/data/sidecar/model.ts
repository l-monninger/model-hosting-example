import React, { useEffect, useReducer, useState } from "react";
import { SidecarLine, ModelConfig } from "../../util";
import { getSidecarApplyConnection, getSidecarDestroyConnection, getSidecarObserverConnection  } from "./lines";
import { useSidecarUrl } from "../deployer/sidecarUrl";

export const useModelLifecyle = (modelId : string, size : number = 1024) : {
    sidecarLines : SidecarLine[],
    apply ? : (config : ModelConfig)=>Promise<void>,
    destroy ? : ()=>Promise<void>
} =>{

    // get the url of the sidecar
    const { getSidecarUrl } = useSidecarUrl();
    const sidecarUrl = getSidecarUrl(modelId);
    const wsUrl = sidecarUrl ? sidecarUrl.replace("http", "ws") : undefined;

    // to initiate socket transitions
    const [needsSocket, setNeedsSocket] = useState(true);

    // reducer will slice out older lines
    const [lines, addSidecarLine] = useReducer((oldSidecarLines : SidecarLine[], line : SidecarLine) : SidecarLine[]=>{
        const _lines = oldSidecarLines.reverse().slice(0, size-1).reverse();
        return [
            ..._lines,
            line
        ]

    }, []);

    // 
    const [funcs, setFuncs] = useState<{
        apply ? : (config : ModelConfig)=>Promise<void>,
        destroy ? : ()=>Promise<void>
    }>({});

    useEffect(()=>{

        let timeout : number | undefined = undefined;
        
        if(needsSocket && wsUrl){

            let ws = getSidecarObserverConnection(wsUrl);

            ws.onopen = ()=>{

                setFuncs({
                    apply : async (config : ModelConfig)=>{

                        await new Promise(async (resolve)=>{

                            let applyWs = getSidecarApplyConnection(wsUrl);
                            applyWs.onmessage = (message)=>{
                        
                            }
                            applyWs.onopen = ()=>{
                           
                                applyWs.send(JSON.stringify(config));
                            }
                            applyWs.onclose = ()=>{
                                resolve(0);
                            }
                        });
        
                    },
                    destroy : async ()=>{

                        await new Promise(async (resolve)=>{
                            let destroyWs = getSidecarDestroyConnection(wsUrl);
                            destroyWs.onmessage = ()=>{
                                destroyWs.close();
                            }
                            destroyWs.onclose = ()=>{
                                resolve(0);
                            }
                        });
    
                    }
                });

            }

            ws.onmessage = (msg)=>{
                
                addSidecarLine(JSON.parse(msg.data) as SidecarLine)
            }

            ws.onclose = ()=>{
                
                timeout = setTimeout(()=>{
                    setNeedsSocket(false);
                    setFuncs({})
                }, 100);

            }   
    
            setNeedsSocket(false);

        }

        return ()=>{
            if(timeout) clearTimeout(timeout);
        }

    }, [sidecarUrl, needsSocket])

    return {
        sidecarLines : lines,
        ...funcs
    };
}