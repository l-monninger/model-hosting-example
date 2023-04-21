import React, { useEffect, useReducer, useState } from "react";
import { ModelConfig } from "../../util";
import { getRuntimeBranchesConnection, useBranches, } from "./branches";
import { getRuntimeSummaryConnection, useSummary } from "./summary";
import { promptModel } from "./prompt";
import { useRuntimeUrl } from "../deployer/runtimeUrl";

const edeps : any[] = [];

export const useModelData = (modelId : string, size : number = 1024) : {
    branchesHistory : string[][],
    branches : string[],
    summaryHistory : string[],
    summary : string,
    prompt : (prompt : string)=>Promise<void>,
} =>{

    const {getRuntimeUrl} = useRuntimeUrl();
    const runtimeUrl = getRuntimeUrl(modelId);

    const {
        branches,
        branchesHistory
    } = useBranches(modelId)

    const {
        summary,
        summaryHistory
    } = useSummary(modelId);

    const [funcs, setFuncs] = useState<{
        prompt : (prompt : string)=>Promise<void>,
    }>({
        prompt : async (prompt : string)=>{

        }
    });

    useEffect(()=>{
        if(runtimeUrl){
            setFuncs({
                prompt : async (prompt : string)=>{
                    await promptModel(prompt, runtimeUrl)
                }
            })
        }
    }, [runtimeUrl])

    return {
        branchesHistory,
        branches,
        summaryHistory,
        summary,
        ...funcs
    };
}