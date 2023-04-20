import React, {FC, ReactElement} from 'react';
import { TextField } from "@mui/material";
import { Button } from '../../components/input/Button/Button';

export const HOME_CLASSNAMES : string[] = [ ];
export const HOME_STYLE : React.CSSProperties = {
    height : "100vh",
    width : "100vw",
    display : "grid",
    alignItems : "center",
    alignContent : "center",
    justifyContent : "center",
    justifyItems : "center"
};

export type HomeProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    onPromptChange ? : (prompt : string)=>Promise<void>;
    onLaunch ? : ()=>Promise<void>;
    disabled ? : boolean;
};

export const Home : FC<HomeProps>  = (props) =>{

    const _handlePromptChange = (event : React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>)=>{
        if(props.onPromptChange)
            props.onPromptChange(event.target.value)
    }

    return (
        <div
        className={[...!props.overrideClasses ? HOME_CLASSNAMES : [], ...props.classNames||[]].join(" ")}
        style={{...!props.overrideStyle ? HOME_STYLE : {}, ...props.style}}>
            <div style={{
                display : "grid",
                height : "200px",
                gridTemplateRows : "1fr 1fr"
            }}>
                <div>
                    <h2>Branch and Summarize</h2>
                </div>
                <div style={{
                    display : "grid",
                    gridTemplateColumns : "1fr"
                }}>
                    <div>
                        <TextField
                        disabled={props.disabled} 
                        style={{
                            width : "400px"
                        }} onChange={_handlePromptChange} id="standard-basic" label="Provide prompt..." variant="standard" />
                    </div>
                    <div style={{
                        display : "grid",
                        justifyContent : "end"
                    }}>
                        <Button 
                        disabled={props.disabled}
                        variant='contained' color='success' aonClick={props.onLaunch}>
                            Launch
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    )
};