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

@app.post("/api/log")
def log_data(data: dict):
    # Here you would handle the incoming data, e.g., save it to a database or file
    print("Received data:", data)
    return {"status": "success", "data": data}

def run():
    uvicorn.run("torchscope.main:app", host="127.0.0.1", port=8000, reload=True)

