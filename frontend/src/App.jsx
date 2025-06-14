// App.jsx or App.tsx
import Navbar from "./Navbar";
import GridBackground from "./GridBackground";
import LinePlot from "./plots/LinePlot";
import DynamicParameters from "./DynamicParameters";    
import React, { useEffect, useState } from 'react';


function App() {
    const [data, setData] = useState(null);

    useEffect(() => {
        const interval = setInterval(() => {
            fetch('http://localhost:8000/data')
                .then(res => res.json())
                .then(json => setData(json))
                .catch(console.error);
        }, 30); // poll every 3 seconds

        return () => clearInterval(interval);
    }, []);
    console.log(data);
    if (!data) {
        return (
            <div className="loader-container">
                <div className="loader">
                    <img
                        src="/logo.png"
                        alt="Loading"
                        className="w-50 h-50 p-2 rounded-full object-cover animate-spin"
                    />
                </div>
            </div>
        );
    }
    return (
        <div className="bg-base w-screen h-screen flex flex-col items-center pr-8 pl-8">
            <Navbar projects={data.projects} models={data.models} runs={data.runs} />
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
                <DynamicParameters params={data.dynamic_params}/> 
            </div>
        </div>
    );
}



export default App;

