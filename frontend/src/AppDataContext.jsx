import React, { createContext, useContext, useState, useRef, useEffect, useCallback } from 'react';
import Loading from './Loading.jsx';

const AppDataContext = createContext();

export function AppDataProvider({ children }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true); // initially loading

    const ws = useRef(null);
    const [graphs, setGraphs] = useState([]);

    useEffect(() => {
        // Connect to the backend WebSocket
        ws.current = new WebSocket("ws://localhost:8000/ws");

        ws.current.onopen = () => {
            console.log("WebSocket connected");
            // wait for a message from the backend 
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
            }
        };
        ws.current.onclose = () => console.log("WebSocket disconnected");


        return () => ws.current.close();
    }, []);



    const refreshData = useCallback(async () => {
        try {
            setLoading(true);
            const res = await fetch('http://localhost:8000/frontend/api/data');
            const json = await res.json();
            setData(json);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
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
            await refreshData();  // Wait for refreshData to finish before continuing
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    }, [refreshData]);

    const selectInstance = useCallback(async (name, item) => {
        try {
            setLoading(true);
            const res = await fetch('http://localhost:8000/frontend/api/selected-instance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: name, selection: item}),
            });
            console.log(res);
            await refreshData();  // Wait for refreshData to finish before continuing
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    }, [refreshData]);


    React.useEffect(() => {
        refreshData();
    }, [refreshData]);

    return (
        <AppDataContext.Provider value={{ data, refreshData, loading, updateParameter, selectInstance, graphs }}>
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

