import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AppDataProvider } from './AppDataContext.jsx'

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <AppDataProvider>
            <App />
        </AppDataProvider>
    </StrictMode>,
)
