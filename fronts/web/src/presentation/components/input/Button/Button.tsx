import React, {FC, ReactElement, useState, useEffect} from 'react';
import { LoadingButton, LoadingButtonProps } from "@mui/lab";
import { X } from "react-bootstrap-icons";

export const BUTTON_CLASSNAMES : string[] = [ ];
export const BUTTON_STYLE : React.CSSProperties = {
};

export type ButtonProps = LoadingButtonProps &{
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    aonClick ? : (e : React.MouseEvent<HTMLButtonElement, MouseEvent>)=>Promise<void>;
};

export const Button : FC<ButtonProps>  = (props) =>{

    const [status, setStatus] = useState(0);

    const handleAonClick = (e : React.MouseEvent<HTMLButtonElement, MouseEvent>)=>{
        
        setStatus(1);
        if(props.aonClick)
            props.aonClick(e)
            .then(()=>setStatus(0))
            .catch(()=>setStatus(2))

    }

    useEffect(()=>{

        let timeout : number | undefined = undefined;

        if (status === 2)
            timeout = setTimeout(()=>setStatus(0), 200);

        return ()=>{if(timeout) clearTimeout(timeout);};

    })

    const {
        aonClick,
        ...primitiveProps
    } = props;

    return (
        <LoadingButton onClick={props.aonClick ? handleAonClick : undefined} {...primitiveProps} loading={status === 1||props.loading} >
            {status === 2 ? <X/> : props.children}
        </LoadingButton>
    )
};