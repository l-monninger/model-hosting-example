import React, {FC, ReactElement} from 'react';
import { ConfigurationForm } from '../ConfigurationForm/ConfigurationForm';
import { SidecarLog } from '../SidecarLog/SidecarLog';
import { ModelConfig, SidecarLine } from '../../../../util';

export const CONFIGURATION_SECTION_CLASSNAMES : string[] = [ ];
export const CONFIGURATION_SECTION_STYLE : React.CSSProperties = {
    display : "grid",
    gridTemplateColumns : "1fr"
};

export type ConfigurationSectionProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    onApply ? : (config : ModelConfig)=>Promise<void>;
    onDestroy ? : ()=>Promise<void>;
    sidecarLines ? : SidecarLine[];
};

export const ConfigurationSection : FC<ConfigurationSectionProps>  = (props) =>{

    return (
        <div
        className={[...!props.overrideClasses ? CONFIGURATION_SECTION_CLASSNAMES : [], ...props.classNames||[]].join(" ")}
        style={{...!props.overrideStyle ? CONFIGURATION_SECTION_STYLE : {}, ...props.style}}>
            <ConfigurationForm 
            onApply={props.onApply}
            onDestroy={props.onDestroy}
            />
            <h4>Log</h4>
            <div style={{
                background : "#f0f0f0",
                padding : 10,
                maxHeight : "200px",
                overflow : "scroll"
            }}>
                <SidecarLog sidecarLines={props.sidecarLines}/>
            </div>
        </div>
    )
};