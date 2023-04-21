import React, { useEffect, useReducer, useState, useRef, useMemo } from "react";
import axios from "axios";
import { useLatentCache } from "../util/useLatentCache";

export const getRuntimeUrlPath = (id : string)=>{
    return `${import.meta.env.VITE_DEPLOYER_PATH}/model_url/${id}`;
}

export const getRuntimeUrl = async (id : string) : Promise<string> =>{

    const res = await axios.get(getRuntimeUrlPath(id));
    return res.data

}

export const RuntimeUrls : {[key : string] : [
    string | undefined, number
]} = {

}

export const useRuntimeUrl = (latency : number = 10_000) : {
    getRuntimeUrl : (id : string, force ? : boolean)=> (string|undefined )
} =>{

    const { get } = useLatentCache<string, string>({
        getter : getRuntimeUrl,
        cache : RuntimeUrls
    })

    return {
        getRuntimeUrl : get
    }

}