import React, { useEffect, useReducer, useState } from "react";
import { SidecarLine, ModelConfig } from "../../util";
import { useRuntimeUrl } from "../deployer/runtimeUrl";

export const getRuntimeSummaryConnection = (url : string)=>{
    return new WebSocket(`${url}/summary`)
}

export const useSummary = (modelId : string, size : number = 1024) : {
    summaryHistory : string[],
    summary : string,
} =>{

    // get the url of the runtime
    const { getRuntimeUrl } = useRuntimeUrl();
    const runtimeUrl = getRuntimeUrl(modelId);
    const wsUrl = runtimeUrl ? runtimeUrl.replace("http", "ws") : undefined;

    // to initiate socket transitions
    const [needsBranchSocket, setNeedsBranchSocket] = useState(true);
    const [summary, addSummary] = useReducer((oldBranchLines : string[], line : string) : string[]=>{
        const _lines = oldBranchLines.reverse().slice(0, size-1).reverse();
        return [
            ..._lines,
            line
        ]

    }, []);

    // summary socket
    useEffect(()=>{

        let timeout : number | undefined = undefined;
        
        if(!!(needsBranchSocket && wsUrl)){

            let ws = getRuntimeSummaryConnection(wsUrl);
     
            ws.onopen = ()=>{
        
            }

            ws.onmessage = (msg)=>{
                addSummary(JSON.parse(msg.data) as string)
            }

            ws.onclose = ()=>{
                timeout = setTimeout(()=>{
                    setNeedsBranchSocket(false);
                }, 100);
            }   
    
            setNeedsBranchSocket(false);

        }

        return ()=>{
            if(timeout) clearTimeout(timeout);
        }

    }, [runtimeUrl, needsBranchSocket]);

    
    return {
        summaryHistory : summary,
        summary : summary[summary.length - 1],
    };
}