import React, {FC, ReactElement} from 'react';
import { BasData } from '../BasData/BasData';
import { TextField } from '@mui/material';
import { Button } from "../../../components/input/Button/Button";


export const BAS_SECTION_CLASSNAMES : string[] = [ ];
export const BAS_SECTION_STYLE : React.CSSProperties = {
};

export type BasSectionProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    branches ? : string[];
    summary ? : string;
    onPrompt ? : ()=>Promise<void>;
    onPromptChange ? : (prompt : string)=>Promise<void>;
};

export const BasSection : FC<BasSectionProps>  = (props) =>{

    const handleTextFieldChange = (e : React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>)=>{
        if(props.onPromptChange)
            props.onPromptChange(e.target.value)
    }

    return (
        <div
        className={[...!props.overrideClasses ? BAS_SECTION_CLASSNAMES : [], ...props.classNames||[]].join(" ")}
        style={{...!props.overrideStyle ? BAS_SECTION_STYLE : {}, ...props.style}}>
            <div style={{
                display : "grid",
                gap : 5
            }}>
                <TextField
                multiline
                rows={10}
                onChange={handleTextFieldChange}
                //disabled={props.disabled} 
                style={{
                    width : "100%"
                }} /*onChange={_handlePromptChange}*/ id="standard-basic" label="Provide prompt or feedback..." variant="outlined" />
                <div style={{
                    width : "100%",
                    display : "flex",
                    justifyContent : "end",
                    justifyItems : "end"
                }}>
                     <Button 
                    style={{
                        height : "100%"
                    }}
                    // disabled={props.disabled}
                    variant='contained' color='success' 
                    aonClick={props.onPrompt}
                    >
                        Send
                    </Button>
                </div>
            </div>
            <br/>
            <BasData 
            branches={props.branches}
            summary={props.summary}
            style={{
                background : "#f0f0f0"
            }}/>
        </div>
    )
};