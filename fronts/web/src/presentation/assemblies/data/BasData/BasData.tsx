import React, {FC, ReactElement} from 'react';
import { Select, MenuItem, InputLabel, Card, CardContent, CardHeader, Box, Accordion, AccordionSummary, AccordionDetails } from "@mui/material";
import { generate } from 'shortid';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';

export const BAS_DATA_CLASSNAMES : string[] = [ ];
export const BAS_DATA_STYLE : React.CSSProperties = {
    display : "grid",
    alignContent : "center",
    alignItems : "center",
    justifyItems : 'center',
    justifyContent : "center",
    padding : 5,
    gridTemplateColumns : "10fr 1fr 10fr",
    gap : 5,
    height : "400px",
};

export type BasDataProps = {
     children ? : React.ReactNode;
    style ? : React.CSSProperties;
    overrideStyle ? : boolean;
    classNames ? : string[];
    overrideClasses ? : boolean;
    responsive ? : boolean;
    branches ? : string[];
    summary ? : string;
};

export const BasData : FC<BasDataProps>  = (props) =>{

    const _summary = props.summary||"N/A";
    const _branches = props.branches||Array(1).fill("N/A");

    return (
        <div
        className={[...!props.overrideClasses ? BAS_DATA_CLASSNAMES : [], ...props.classNames||[]].join(" ")}
        style={{...!props.overrideStyle ? BAS_DATA_STYLE : {}, ...props.style}}>
             <div style={{
                }}>
                    <Card style={{
                        height : "300px",
                        width : "300px",
                        overflowY : "scroll"
                    }}>
                        <CardContent>
                            <h4>Summary</h4>
                            {_summary}
                        </CardContent>
                    </Card>
                </div>
                <div>
                    <SwapHorizIcon/>
                </div>
                <div style={{
                    display : "grid",
                    gridTemplateColumns : "1fr",
                    gap : 5,
                    maxHeight : 400,
                    minHeight : 304,
                    overflowX : "visible",
                    overflowY : "scroll",
                    justifyItems : "center",
                    justifyContent : "center"
                }}>
                    {_branches.map((branch, i)=>{

                        return <Card 
                            style={{
                                height : "300px",
                                width : "300px",
                                overflowY : "scroll"
                            }}
                            key={generate()}>
                            <CardContent>
                                <h4>Branch #{i + 1}</h4>
                                {branch}
                            </CardContent>
                        </Card>

                    })}
                </div>
        </div>
    )
};