// App.jsx or App.tsx
import Navbar from "./Navbar";
import GridBackground from "./GridBackground";
import LinePlot from "./plots/LinePlot";
import DynamicParameters from "./DynamicParameters";    
import React, { useEffect, useState, useRef } from 'react';
import Loading from "./Loading";
import { useAppData } from "./AppDataContext";


function App() {
    const { data } = useAppData();


    const ws = useRef(null);

    useEffect(() => {
        // Connect to the backend WebSocket
        ws.current = new WebSocket("ws://localhost:8000/ws");

        ws.current.onopen = () => {
            console.log("WebSocket connected");
            sendMessage();
        }
        ws.current.onmessage = (event) => {
            console.log("Received message:", event.data);
            sendMessage();
        };
        ws.current.onclose = () => console.log("WebSocket disconnected");

        return () => ws.current.close();
    }, []);

    const sendMessage = () => {
        console.log("Sending message");
        if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send("Hello from frontend");
            console.log("Message sent");
        }
    };


    return (
        <div className="bg-base w-screen h-screen flex flex-col items-center pr-8 pl-8">
            <Navbar data={data} />
            <div className="w-full h-full relative">
                <GridBackground />
                {data.line_plots.map((plot, index) => (
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

