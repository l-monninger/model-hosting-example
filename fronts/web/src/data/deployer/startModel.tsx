import React, { useEffect, useReducer, useState } from "react";
import axios from "axios";
import { StartModelConfig } from "../../util";
import { generate } from "shortid";

export const startModelPath = ()=>{
    return `${import.meta.env.VITE_DEPLOYER_PATH}/start_model`;
}

export const startModel = async (config : StartModelConfig) : Promise<string> =>{

    const res = await axios.post(startModelPath(), config);
    return res.data

}