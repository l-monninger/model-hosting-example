import React, {FC, ReactElement} from 'react';
import { CircularProgress } from '@mui/material';
import { ExclamationCircleFill, CheckCircleFill } from 'react-bootstrap-icons';
import Ansi from "ansi-to-react";

export const SIDECAR_LINE_CLASSNAMES : string[] = [ ];
export const SIDECAR_LINE_STYLE : React.CSSProperties = {
    display : "flex",
    // alignContent : "center",
    // alignItems : "center"
};

export type SidecarLineProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    status ? : number;
    line ? : string;
    statusSize ? : number;
    statusWidth ? : number;
};

export const SidecarLine : FC<SidecarLineProps>  = (props) =>{

    const _status = props.status??2;
    const _line = props.line||"Awaiting log...";

    const _statusSize = props.statusSize??14;
    const _statusWidth = props.statusWidth??30;

    const StatusIcon = 
    _status === 0 ? <CheckCircleFill color='#44cc88' size={_statusSize}/>
    : _status === 1 ? <ExclamationCircleFill color='#cc4444' size={_statusSize}/>
    : <CircularProgress style={{
        fill : 'purple'
    }} size={_statusSize}/>;

    return (
        <div
        className={[...!props.overrideClasses ? SIDECAR_LINE_CLASSNAMES : [], ...props.classNames||[]].join(" ")}
        style={{...!props.overrideStyle ? SIDECAR_LINE_STYLE : {}, ...props.style}}>
            <div style={{
                width : _statusWidth
            }}>
                {_line.length > 0 ? StatusIcon : <></>}
            </div>
            <Ansi>
                {_line}
            </Ansi>
        </div>
    )
};