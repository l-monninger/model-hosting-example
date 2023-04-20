import React, { useEffect, useReducer, useState } from "react";
import axios from "axios";
import { StartModelConfig } from "../../util";
import { generate } from "shortid";
import {to} from "await-to-js"

export const promptModelPath = (url : string)=>{
    return `${url}/prompt`;
}

export const promptModel = async (prompt : string, url : string) : Promise<string> =>{

    const res = await axios.post(promptModelPath(url), {
        prompt : prompt
    });
    return res.data

}