import React, { useEffect, useReducer, useState } from "react";
import { useRuntimeUrl } from "../deployer/runtimeUrl";

export const getRuntimeBranchesConnection = (url : string)=>{
    return new WebSocket(`${url}/branches`)
}

export const useBranches = (modelId : string, size : number = 1024) : {
    branchesHistory : string[][],
    branches : string[],
} =>{

    // get the url of the runtime
    const { getRuntimeUrl } = useRuntimeUrl();
    const runtimeUrl = getRuntimeUrl(modelId);
    const wsUrl = runtimeUrl ? runtimeUrl.replace("http", "ws") : undefined;

    // to initiate socket transitions
    const [needsBranchSocket, setNeedsBranchSocket] = useState(true);
    const [branches, addBranches] = useReducer((oldBranchLines : string[][], line : string[]) : string[][]=>{
        const _lines = oldBranchLines.reverse().slice(0, size-1).reverse();
        return [
            ..._lines,
            line
        ]

    }, []);

    // branches socket
    useEffect(()=>{

        let timeout : number | undefined = undefined;
        
        if(!!(needsBranchSocket && wsUrl)){

            let ws = getRuntimeBranchesConnection(wsUrl);
     
            ws.onopen = ()=>{

            }

            ws.onmessage = (msg)=>{
                addBranches(JSON.parse(msg.data) as string[])
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
        branchesHistory : branches,
        branches : branches[branches.length - 1],
    };
}