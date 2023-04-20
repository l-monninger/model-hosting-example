import React, { useEffect, useReducer, useState } from "react";
import axios from "axios";

export const getRuntimeUrlPath = (url : string)=>{
    return `${url}/model_url`;
}

export const getRuntimeUrl = async (url : string) : Promise<string> =>{

    const res = await axios.get(getRuntimeUrlPath(url));
    return res.data

}

export const useRuntimeUrl = (size : number = 5) : {
    getRuntimeUrl : (url : string)=> (string|undefined )
} =>{

    const [runtimeUrls, setRuntimeUrls] = useState<{
        [key : string] : string
    }>({});

    return {
        getRuntimeUrl : (
            url : string
        ) : string|undefined =>{
    
    
            getRuntimeUrl(url)
            .then((res)=>{
                setRuntimeUrls({
                    ...runtimeUrls,
                    [url] : res
                })
            });
    
            return runtimeUrls[url];
    
        }
    }

}