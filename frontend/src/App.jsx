// App.jsx
import Plot from 'react-plotly.js'
import { useState } from 'react'
import axios from 'axios'

function App() {
  const [step, setStep] = useState(0)
  const [loss, setLoss] = useState(0.0)
  const [response, setResponse] = useState(null)

  const sendMetric = async () => {
    const res = await axios.post('http://localhost:8000/api/log', {
      step: parseInt(step),
      loss: parseFloat(loss)
    })
    setResponse(res.data)
  }

  const steps = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  const losses = [0.95, 0.82, 0.74, 0.63, 0.51, 0.43, 0.37, 0.30, 0.24, 0.20]

  return (
    <div style={{ padding: 20 }}>
      <h1>TorchScope</h1>
      <input type="number" value={step} onChange={(e) => setStep(e.target.value)} placeholder="Step" />
      <input type="number" value={loss} onChange={(e) => setLoss(e.target.value)} placeholder="Loss" />
      <button onClick={sendMetric}>Send Metric</button>
      {response && <pre>{JSON.stringify(response, null, 2)}</pre>}

      <Plot
        data={[
          {
            x: steps,
            y: losses,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Loss',
            line: { color: '#e76f51' },
            marker: { size: 6 }
          }
        ]}
        layout={{
          title: 'Training Loss',
          xaxis: {
            title: 'Step',
            rangeslider: false
          },
          yaxis: {
            title: 'Loss'
          },
          dragmode: 'zoom', // Enables box zoom
          responsive: true
        }}
        config={{
          scrollZoom: true, // Enables scroll wheel zoom
          displayModeBar: true, // Toolbar with zoom/pan/export
        }}
        style={{ width: '100%', height: '400px' }}
      />
    </div>
  )
}

export default App

