import React, {FC, ReactElement} from 'react';
import { SidecarLine } from '../../../../util';
import { SidecarLine as SidecarLogLine } from '../SidecarLine/SidecarLine';
import { generate } from 'shortid';

export const SIDECAR_LOG_CLASSNAMES : string[] = ["log-scroller" ];
export const SIDECAR_LOG_STYLE : React.CSSProperties = {
   //  display : 'grid',
    // gridTemplateColumns : "1fr",
};

export type SidecarLogProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    sidecarLines ? : SidecarLine[];
};

export const SidecarLog : FC<SidecarLogProps>  = (props) =>{

    const _lines = !props.sidecarLines || (props.sidecarLines.length < 1) 
    ? [[undefined, undefined]] : props.sidecarLines;
    const Lines = _lines.map(([status, line])=>{
        return <SidecarLogLine classNames={["log-item"]} key={generate()} status={status} line={line}/>
    })

    return (
        <div
        className={[...!props.overrideClasses ? SIDECAR_LOG_CLASSNAMES : [], ...props.classNames||[]].join(" ")}
        style={{...!props.overrideStyle ? SIDECAR_LOG_STYLE : {}, ...props.style}}>
            <div className='log-scroller-content'>
                {Lines}
            </div>
        </div>
    )
};