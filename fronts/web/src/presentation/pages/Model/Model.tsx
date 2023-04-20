import React, {FC, ReactElement} from 'react';
import { ModelConfig, SidecarLine } from '../../../util';
import { Select, MenuItem, InputLabel, Card, CardContent, CardHeader, Box, Accordion, AccordionSummary, AccordionDetails } from "@mui/material";
import { Button } from '../../components/input/Button/Button';
import { generate } from 'shortid';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';
import { ConfigurationForm } from '../../assemblies/configuration/ConfigurationForm/ConfigurationForm';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { BasData } from '../../assemblies/data/BasData/BasData';
import { ConfigurationSection } from '../../assemblies/configuration/ConfigurationSection';
import { BasSection } from '../../assemblies/data/BasSection/BasSection';

export const MODEL_CLASSNAMES : string[] = [ ];
export const MODEL_STYLE : React.CSSProperties = {
    height : "100vh",
    width : "100vw",
    padding : 10, 
    justifyContent : "center",
    justifyItems : "center",
    overflowY : "scroll"
};

export type ModelProps = {
    children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    sidecarLines ? : SidecarLine[];
    config ? : ModelConfig;
    onConfigUpdate ? : (config : ModelConfig)=>Promise<void>;
    onApply ? : (config : ModelConfig)=>Promise<void>;
    onDestroy ? : ()=>Promise<void>;
    onPromptChange ? : (prompt : string)=>Promise<void>;
    onPrompt ? : ()=>Promise<void>;
    branches ? : string[];
    summary ? : string;
};

export const Model : FC<ModelProps>  = (props) =>{


    return (
        <div
        className={[...!props.overrideClasses ? MODEL_CLASSNAMES : [], ...props.classNames||[]].join(" ")}
        style={{...!props.overrideStyle ? MODEL_STYLE : {}, ...props.style}}>
            <div style={{
                display : "grid",
                width : "60%",
                gridTemplateColumns : "1fr",
                margin : "0 auto"
            }}>
                <h2>Branch and Summarize</h2>
                <Accordion style={{
                    width : "100%",
                    background : "#f9f9f9"
                }}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                        <h3>Configuration</h3>
                    </AccordionSummary>
                    <AccordionDetails>
                        <ConfigurationSection 
                        sidecarLines={props.sidecarLines} 
                        onApply={props.onApply}
                        onDestroy={props.onDestroy}/>
                    </AccordionDetails>
                </Accordion>
                <Accordion style={{
                    width : "100%",
                    background : "#f9f9f9"
                }} >
                    <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                        <h3>Dialogue</h3>
                    </AccordionSummary>
                    <AccordionDetails>
                        <BasSection 
                            summary={props.summary}
                            branches={props.branches}
                            onPromptChange={props.onPromptChange}
                            onPrompt={props.onPrompt}/>
                    </AccordionDetails>
                </Accordion>
            </div>
        </div>
    )
};