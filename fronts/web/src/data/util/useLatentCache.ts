import React, { useEffect, useReducer, useState, useRef, useMemo } from "react";
import axios from "axios";
import { RuntimeUrls } from "../deployer/runtimeUrl";

export type LatentCache<V extends any> = {[key : string] : [V | undefined, number]};
export type CacheDef<K extends any, V extends any> = {
    cache : LatentCache<V>,
    getter : (key : K)=>Promise<V>,
    hash  : (key : K)=>string,
    latency : number
}

export const _flag = <V>(
    hash : string,
    cache : LatentCache<V>
) => {

    const res = cache[hash]
    if(!res) cache[hash] = [undefined, performance.now()];
    else cache[hash][1] = performance.now()

}

export const _setCache = <V>(
    hash : string, val : V | undefined,
    cache : LatentCache<V>
) =>{

    cache[hash] = [val, performance.now()];
 
}

export const _readThrough = async <K, V>(
    hash : string,
    key : K,
    cache : CacheDef<K, V>,
    notify : ()=>void
) : Promise<void> => {

    const res = await cache.getter(key)
    _setCache(
        hash,
        res,
        cache.cache
    );
    notify();

}

export const getThroughCache = <K, V>(
    key : K,
    cache : CacheDef<K, V>,
    notify : ()=>void
) : V | undefined =>{

    const hash = cache.hash(key);

    // check if it exists at all
    const res = cache.cache[hash];
    if(!res) {
        _setCache(hash, undefined, cache.cache);
        _readThrough(
            hash,
            key,
            cache,
            notify
        );
        return undefined;
    }

    // unpack value and timestamp
    const [val, ts] = res
    
    if(performance.now() - ts > cache.latency){
        _setCache(hash, undefined, cache.cache);
        _readThrough(
            hash,
            key,
            cache,
            notify
        );
        return undefined;

    };

    console.log(val)
    return val;
 
}

export const useLatentCache = <K extends any, V extends any>({
    cache,
    getter,
    hash = (key : K)=>key as string,
    latency = 10_000
} : {
    cache : LatentCache<V>,
    getter : (key : K)=>Promise<V>,
    hash ? : (key : K)=>string,
    latency ? : number
})=>{

    const [tick, increment] = useReducer(x=>x+1, 0);
    console.log("USING LATENT CACHE: ", tick, getter)

    return {
        get : (
            id : K
        ) : V|undefined =>getThroughCache(
            id,
            {
                cache,
                getter,
                hash,
                latency,
            },
            increment
           )
                
    }

}