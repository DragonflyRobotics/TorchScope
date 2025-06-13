from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import duckdb as db 

db_conn = db.connect("torchscope.db")

app = FastAPI()
# Allow your React dev server origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React default dev server origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc)
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "TorchScope backend running!"}


data = {
    "projects": ["jarvis", "torchscope", "torchscope2"],
    "models": ["resnet18", "resnet34", "resnet50", "resnet101", "resnet152"],
    "runs": ["run1", "run2", "run3"],
    "line_plots": [
        {"x": [1, 2, 3], "y": [4, 5, 6], "name": "Line Plot 1"},
        {"x": [1, 2, 3], "y": [6, 5, 4], "name": "Line Plot 2"}
    ],
    "dynamic_params": [
        {"name": "learning_rate", "value": 0.001, "min": 0.0001, "max": 0.01, "step": 0.0001},
        {"name": "batch_size", "value": 32, "min": 8, "max": 128, "step": 8},
        {"name": "num_epochs", "value": 10, "min": 1, "max": 100, "step": 1}
    ]
}

@app.get("/data")
def get_data():
    for plot in data["line_plots"]:
        plot["x"].append(plot["x"][-1] + 1)
        plot["y"].append(plot["y"][-1] + 1)
    return data

@app.post("/api/update-parameter") # currently doesn't use python value after first load
def set_params(params: dict): 
    # Here you would typically save the parameters to a database or file
    print("Received parameters:", params)
    return {"status": "success", "message": "Parameters saved successfully"}

@app.post("/api/selected-project")
def set_project(params: dict): 
    # Here you would typically save the parameters to a database or file
    print("Received parameters:", params)
    return {"status": "success", "message": "Parameters saved successfully"}

@app.post("/api/selected-model")
def set_model(params: dict): 
    # Here you would typically save the parameters to a database or file
    print("Received parameters:", params)
    return {"status": "success", "message": "Parameters saved successfully"}

@app.post("/api/selected-run")
def set_run(params: dict): 
    # Here you would typically save the parameters to a database or file
    print("Received parameters:", params)
    return {"status": "success", "message": "Parameters saved successfully"}

def run():
    uvicorn.run("torchscope.main:app", host="127.0.0.1", port=8000, reload=True)

