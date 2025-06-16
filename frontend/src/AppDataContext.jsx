import React, { createContext, useContext, useState, useRef, useEffect, useCallback } from 'react';
import Loading from './Loading.jsx';

const AppDataContext = createContext();

export function AppDataProvider({ children }) {
    const [data, setData] = useState(
        {
            "dynamic_params": [
                { "name": "learning_rate", "value": 0.001, "min": 0.0001, "max": 0.01, "step": 0.0001 },
                { "name": "learning_rate", "value": 0.001, "min": 0.0001, "max": 0.01, "step": 0.0001 },
                { "name": "learning_rate", "value": 0.001, "min": 0.0001, "max": 0.01, "step": 0.0001 },
            ],
        }
    );
    const [loading, setLoading] = useState(false); // initially loading

    const [selectedProject, setSelectedProject] = useState(null);
    const [selectedModel, setSelectedModel] = useState(null);
    const [selectedRun, setSelectedRun] = useState(null);

    const [projects, setProjects] = useState([]);
    const [models, setModels] = useState([]);
    const [runs, setRuns] = useState([]);

    useEffect(() => {
        // Fetch projects from the backend
        fetch('http://localhost:8000/frontend/api/projects')
            .then(res => res.json())
            .then((res) => setProjects(res))
            .catch(err => console.error(err));
    }, []);
    useEffect(() => {
        console.log("project selected", selectedProject);
        setModels([]);
        setRuns([]);
        setSelectedModel(null);
        setSelectedRun(null);
        if (!selectedProject) return;
        fetch('http://localhost:8000/frontend/api/models', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project: selectedProject }),
        })
            .then(res => res.json())
            .then((res) => setModels(res))
            .catch(err => console.error(err));
    }, [selectedProject]);

    useEffect(() => {
        console.log("model selected", selectedModel);
        setRuns([]);
        setSelectedRun(null);
        if (!selectedModel) return;
        fetch('http://localhost:8000/frontend/api/runs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model: selectedModel }),
        })
            .then(res => res.json())
            .then((res) => setRuns(res))
            .catch(err => console.error(err));
    }, [selectedModel]);

    useEffect(() => {
        if (selectedRun === null) {
            setGraphs([]);
            if (ws.current) {
                ws.current.send(JSON.stringify({ type: 'selected_run', run: "null" })); // Request initial data
            }
            return;
        }
        ws.current.send(JSON.stringify({ type: 'selected_run', run: selectedRun.toString() })); // Request initial data
    }, [selectedRun]);

    const ws = useRef(null);
    const [graphs, setGraphs] = useState([]);

    useEffect(() => {
        // Connect to the backend WebSocket
        ws.current = new WebSocket("ws://localhost:8000/ws");

        ws.current.onopen = () => {
            console.log("WebSocket connected");
            // This will trigger the backend to send the current data 
            // and update the graph

        }
        ws.current.onerror = (error) => {
            console.error("WebSocket error:", error);
        }
        ws.current.onmessage = (event) => {
            console.log("Received message:", event.data);
            const message = JSON.parse(event.data);
            if (message.type === 'update_graph') {
                console.log("Updating graph with data:", message.data);
                setGraphs(message.data);
            } else if (message.type === 'no_data') {
                console.log("No data received from backend");
                setGraphs([]);
            } else if (message.type === 'request') {
                console.log("Received request for data, sending current data");
            }
        };
        ws.current.onclose = () => console.log("WebSocket disconnected");


        return () => ws.current.close();
    }, []);




    const updateParameter = useCallback(async (name, value) => {
        try {
            setLoading(true);
            const res = await fetch('http://localhost:8000/frontend/api/update-parameter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, value }),
            });
            console.log(res);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    });



    return (
        <AppDataContext.Provider value={{ data, loading, updateParameter, graphs, projects, models, runs, selectedProject, setSelectedProject, selectedModel, setSelectedModel, selectedRun, setSelectedRun }}>
            <>
                {data && children}
                {loading && (
                    <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
                        <Loading />
                    </div>
                )}
            </>
        </AppDataContext.Provider>
    );
}

export function useAppData() {
    return useContext(AppDataContext);
}

