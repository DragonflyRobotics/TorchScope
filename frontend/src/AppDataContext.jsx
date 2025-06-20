import React, { createContext, useContext, useState, useRef, useEffect, useCallback } from 'react';
import Loading from './Loading.jsx';

const AppDataContext = createContext();

export function AppDataProvider({ children }) {
    const clientId = useRef(
        sessionStorage.getItem("torchscope-client-id") || (() => {
            const id = crypto.randomUUID();
            sessionStorage.setItem("torchscope-client-id", id);
            return id;
        })()
    ).current;
    const [data, setData] = useState(
        {
            "dynamic_params": [
                { "name": "smoothing", "value": 0.6, "min": 0.0, "max": 1.0, "step": 0.01 },
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
    const [modelSVG, setModelSVG] = useState(null);

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
        console.log("models", models);
        setRuns([]);
        setSelectedRun(null);
        if (!selectedModel) return;
        fetch('http://localhost:8000/frontend/api/runs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model: models.find(m => m.name === selectedModel)?.model || null }),
        })
            .then(res => res.json())
            .then((res) => {setRuns(res.runs); setModelSVG(res.svg)})
            .catch(err => console.error(err));
    }, [selectedModel]);


    useEffect(() => {
        console.log("run selected", selectedRun);
        console.log("runs", runs);
        if (selectedRun === null) {
            setGraphs([]);
            setModelSVG(null);
            if (ws.current) {
                ws.current.send(JSON.stringify({ type: 'selected_run', run: "null" })); // Request initial data
            }
            return;
        }
        console.log("found", runs.find(r => r.name === selectedRun.toString())?.run);
        ws.current.send(JSON.stringify({ type: 'selected_run', run: runs.find(r => r.name === selectedRun.toString())?.run || null })); // Request initial data
    }, [selectedRun]);

    const ws = useRef(null);
    const [graphs, setGraphs] = useState([]);

    useEffect(() => {
        // Connect to the backend WebSocket
        ws.current = new WebSocket(`ws://localhost:8000/ws?client_id=${clientId}`);

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
            } else if (message.type === 'new_session') {
                console.log("New session started");
                window.location.reload();
            }
        };
        ws.current.onclose = () => console.log("WebSocket disconnected");


        return () => ws.current.close();
    }, []);




    const sendParameter = useCallback(async (name, value) => {
        try {
            setLoading(true);
            const new_data = {
                ...data,
                dynamic_params: data.dynamic_params.map((param) =>
                    param.name === name ? { ...param, value: value } : param
                )
            };
            setData(new_data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    });


    const updateParameter = useCallback(async (name, value) => {
    try {
        setLoading(true);

        const new_data = {
            ...data,
            dynamic_params: data.dynamic_params.map((param) =>
                param.name === name ? { ...param, value } : param
            ),
        };

        setData(new_data);  // local update

        const res = await fetch(`http://localhost:8000/frontend/api/update-parameter?client_id=${clientId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(new_data),
        });

        if (!res.ok) {
            console.error("Error updating parameter:", res.statusText);
        }
    } catch (error) {
        console.error("updateParameter error:", error);
    } finally {
        setLoading(false);
    }
}, [data, clientId]);



    return (
        <AppDataContext.Provider value={{ data, loading, updateParameter, graphs, projects, models, runs, selectedProject, setSelectedProject, selectedModel, setSelectedModel, selectedRun, setSelectedRun, modelSVG }}>
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

