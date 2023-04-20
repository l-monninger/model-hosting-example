import React, {FC, ReactElement} from 'react';
import { Button } from '../../../components/input/Button/Button';
import { ModelConfig, SidecarLine } from '../../../../util';
import { Select, MenuItem, InputLabel, Card, CardContent, CardHeader, Box } from "@mui/material";

export const CONFIGURATION_FORM_CLASSNAMES : string[] = [ ];
export const CONFIGURATION_FORM_STYLE : React.CSSProperties = {
};

export type ConfigurationFormProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    config ? : ModelConfig;
    onConfigUpdate ? : (config : ModelConfig)=>Promise<void>;
    onApply ? : (config : ModelConfig)=>Promise<void>;
    onDestroy ? : ()=>Promise<void>;
    applying ? : boolean;
    destroying ? : boolean;
};

export const ConfigurationForm : FC<ConfigurationFormProps>  = (props) =>{

    const _config = props.config||{
        depth : 1,
        width : 1,
        latency : 10
    };

    return (
        <div style={{
            display : "grid",
            gap : 10,
            ...props.style
        }}>
            <div style={{
                display : "flex",
                gridTemplateColumns : "1fr 1fr 1fr",
                gap : 20,
            }}>
                <div>
                    <InputLabel id={"depth-label"}>Depth</InputLabel> 
                    <Select
                    style={{width : 100}}
                        labelId="depth-label"
                        id="depth"
                        value={_config.depth||1}
                        label="Depth">
                        <MenuItem value={1}>1</MenuItem>
                        <MenuItem value={2}>2</MenuItem>
                        <MenuItem value={3}>3</MenuItem>
                    </Select>
                </div>
                <div>
                    <InputLabel id={"width-label"}>Width</InputLabel> 
                    <Select
                    style={{width : 100}}
                        labelId="width-label"
                        id="width"
                        value={_config.width||1}
                        label="Width">
                        <MenuItem value={1}>1</MenuItem>
                        <MenuItem value={2}>2</MenuItem>
                        <MenuItem value={3}>3</MenuItem>
                    </Select>
                </div>
                <div>
                    <InputLabel id={"latency-label"}>Latency</InputLabel>  
                    <Select
                    style={{width : 100}}
                        labelId="latency-label"
                        id="latency"
                        value={_config.latency||10}
                        label="Latency">
                        <MenuItem value={5}>5s</MenuItem>
                        <MenuItem value={10}>10s</MenuItem>
                        <MenuItem value={30}>30s</MenuItem>
                    </Select>
                </div>
            </div>
            <div>
                <div style={{
                    display : "flex",
                    width : "100%",
                    justifyContent : "end",
                    justifyItems : "end", gap : 5
                }}>
                    <Button
                        loading={props.applying}
                        //disabled={props.disabled}
                        variant='contained' color='error' 
                        aonClick={async ()=>{
                            if(props.onDestroy) await props.onDestroy();
                        }}
                        >
                        Destroy
                    </Button>
                    <Button 
                    loading={props.destroying}
                    //disabled={props.disabled}
                    variant='contained' color='success' 
                    aonClick={async ()=>{
                        if(props.onApply) await props.onApply({});
                    }}
                    >
                        Apply
                    </Button>
                </div>
            </div>  
        </div>
    )
};