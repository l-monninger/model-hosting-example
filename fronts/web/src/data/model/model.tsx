import React, { useEffect, useReducer, useState, useMemo } from "react";
import { useModelLifecyle } from "../sidecar/model";
import { useModelData } from "../runtime/model";
import { SidecarLine } from "../../util";
import { ModelConfig } from "../../util";

export const useModel = (id : string) : {
    sidecarLines : SidecarLine[],
    apply ? : (config : ModelConfig)=>Promise<void>,
    destroy ? : ()=>Promise<void>,
    branchesHistory : string[][],
    branches : string[],
    summaryHistory : string[],
    summary : string,
    prompt : (prompt : string)=>Promise<void>,
}=>{

    const {
        sidecarLines,
        apply,
        destroy
    } = useModelLifecyle(id);

    const {
        branches, branchesHistory,
        summary, summaryHistory,
        prompt
    } = useModelData(id);

    return {
        sidecarLines,
        apply,
        destroy,
        branches, branchesHistory,
        summary, summaryHistory,
        prompt
    }

}