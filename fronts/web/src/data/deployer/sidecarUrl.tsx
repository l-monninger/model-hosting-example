import React, { useEffect, useReducer, useState, useRef, useMemo } from "react";
import axios from "axios";
import { useLatentCache } from "../util/useLatentCache";

export const getSidecarUrlPath = (id : string)=>{
    return `${import.meta.env.VITE_DEPLOYER_PATH}/sidecar_url/${id}`;
}

export const getSidecarUrl = async (id : string) : Promise<string> =>{

    const res = await axios.get(getSidecarUrlPath(id));
    return res.data

}

export const SidecarUrls : {[key : string] : [
    string | undefined, number
]} = {

}

export const useSidecarUrl = (latency : number = 10_000) : {
    getSidecarUrl : (id : string, force ? : boolean)=> (string|undefined )
} =>{

    const {get} = useLatentCache<string, string>({
        getter : getSidecarUrl,
        cache : SidecarUrls
    })

    return {
        getSidecarUrl : get
    };

}