import React, {FC, ReactElement, useEffect, useState} from 'react';
import { Model as ModelPage } from '../../presentation/pages/Model/Model';
import { useParams, useSearchParams } from 'react-router-dom';
import { useModelLifecyle } from '../../data/sidecar/model';
import { ModelConfig } from '../../util';
import { useModel } from '../../data/model/model';

export const MODEL_CLASSNAMES : string[] = [ ];
export const MODEL_STYLE : React.CSSProperties = {
};

export type ModelProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
};

export const Model : FC<ModelProps>  = (props) =>{

    const {id} = useParams();
    const [searchParams, setSearchParams] = useSearchParams();
    const applyPrompt = searchParams.get("prompt");

    const [promptStr, setPrompStr] = useState("");

    const {
        sidecarLines,
        apply,
        destroy,
        branches,
        branchesHistory,
        prompt,
        summary,
        summaryHistory
    } = useModel(id || "-1");

    useEffect(()=>{

        if(apply && applyPrompt && applyPrompt.length){
            apply({
                prompt : applyPrompt
            }).then(()=>{
                setSearchParams({});
            })
        }

    }, [apply])

    const handlePrompt = async ()=>{
        await prompt(promptStr)
    }

    const handlePromptChange = async (prompt : string)=>{
        setPrompStr(prompt)
    }

    return (
        <ModelPage 
            sidecarLines={sidecarLines} 
            onDestroy={destroy}
            onApply={apply}
            branches={branches}
            summary={summary}
            onPrompt={handlePrompt}
            onPromptChange={handlePromptChange}/>
    )
};