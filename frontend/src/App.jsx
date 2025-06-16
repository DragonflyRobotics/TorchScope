// App.jsx or App.tsx
import Navbar from "./Navbar";
import GridBackground from "./GridBackground";
import LinePlot from "./plots/LinePlot";
import DynamicParameters from "./DynamicParameters";    
import React, { useEffect, useState, useRef } from 'react';
import Loading from "./Loading";
import { useAppData } from "./AppDataContext";


function App() {
    const { data, graphs } = useAppData();


    //
    // const sendMessage = () => {
    //     console.log("Sending message");
    //     if (ws.current?.readyState === WebSocket.OPEN) {
    //         ws.current.send("Hello from frontend");
    //         console.log("Message sent");
    //     }
    // };


    return (
        <div className="bg-base w-screen h-screen flex flex-col items-center pr-8 pl-8">
            <Navbar data={data} />
            <div className="w-full h-full relative">
                <GridBackground />
                {graphs.map((plot, index) => (
                    <LinePlot
                        x={plot.x}
                        y={plot.y}
                        name={plot.name}
                    />
                ))
                }
                <DynamicParameters /> 
            </div>
        </div>
    );
}



export default App;

