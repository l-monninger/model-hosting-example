import React, {FC, ReactElement, useState} from 'react';
import { Home as HomePage, HomeProps as HomePageProps } from '../../presentation/pages';
import { startModel } from '../../data/deployer/startModel';
import { useNavigate } from 'react-router-dom';

export const HOME_CLASSNAMES : string[] = [ ];
export const HOME_STYLE : React.CSSProperties = {
};

export type HomeProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
};

export const Home : FC<HomeProps>  = (props) =>{

    const [prompt, setPrompt] = useState("");
    const [disabled, setDiasbled] = useState(false);
    const handlePrompt = async (prompt : string)=>setPrompt(prompt);

    const navigate = useNavigate();

    const onLaunch = async ()=>{
        setDiasbled(true);
        const id = await startModel({
            prompt : prompt.length > 0 ? prompt : undefined
        });
        navigate(`/model/${id}?prompt=${encodeURI(prompt)}`);
    }

    return (
        <HomePage 
            disabled={disabled}
            onLaunch={onLaunch}
            onPromptChange={handlePrompt}/>
    )
};