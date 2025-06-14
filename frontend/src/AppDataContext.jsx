import React, { createContext, useContext, useState, useCallback } from 'react';
import Loading from './Loading.jsx';

const AppDataContext = createContext();

export function AppDataProvider({ children }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true); // initially loading


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
        <AppDataContext.Provider value={{ data, refreshData, loading, updateParameter, selectInstance }}>
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

