from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import duckdb as db
import time
import asyncio

from torchscope.db.utils import drop_run


db_conn = db.connect("torchscope.db")

drop_run(db_conn, 3821)
drop_run(db_conn, 4141)
drop_run(db_conn, 3912)
drop_run(db_conn, 4829)


db_conn.execute(
    """
DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS project_models;
DROP TABLE IF EXISTS timestamp_project;
CREATE TABLE IF NOT EXISTS run_3821 (
   iteration INTEGER,
   lr        FLOAT,
   loss      FLOAT,
   accuracy  FLOAT,
   val_loss  FLOAT
);

CREATE TABLE IF NOT EXISTS run_4141 (
   iteration INTEGER,
   lr        FLOAT,
   loss      FLOAT,
   accuracy  FLOAT
);

CREATE TABLE IF NOT EXISTS run_3912 (
   iteration INTEGER,
   lr        FLOAT,
   loss      FLOAT
);

CREATE TABLE IF NOT EXISTS run_4829 (
   iteration INTEGER,
   lr        FLOAT
);

CREATE TABLE IF NOT EXISTS model_runs (
   runs      INTEGER,
   model     INTEGER,
   timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project_models (
   model     INTEGER,
   project   VARCHAR,
   timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS timestamp_project (
   project   VARCHAR,
   timestamp TIMESTAMP
);

-- run_3821: full training data
INSERT INTO run_3821 VALUES
(1, 0.01, 0.693, 0.50, 0.700),
(2, 0.01, 0.682, 0.55, 0.690),
(3, 0.01, 0.670, 0.60, 0.675);

-- run_3821: full training data
INSERT INTO run_4141 VALUES
(1, 0.01, 0.693, 0.50),
(2, 0.01, 0.682, 0.55),
(3, 0.01, 0.670, 0.60);


-- run_3912: missing accuracy/val_loss
INSERT INTO run_3912 VALUES
(1, 0.01, 0.695),
(2, 0.01, 0.688),
(3, 0.01, 0.673);

-- run_4829: only lr tracked
INSERT INTO run_4829 VALUES
(1, 0.005),
(2, 0.005),
(3, 0.005);

-- model GUIDs (random 4-digit integers)
-- run GUIDs already in use: 3821, 3912, 4829
-- model GUIDs: 1001, 1002, 1003

-- model_runs links runs to models with timestamps
INSERT INTO model_runs VALUES
(3821, 1001, '2024-11-01 14:23:11'),
(4141, 1001, '2024-05-13 10:12:47'),
(3912, 1002, '2024-12-05 10:12:47'),
(4829, 1003, '2025-01-12 09:00:00');

-- project_models links models to projects
INSERT INTO project_models VALUES
(1001, 'torchscope',    '2024-10-12 11:00:00'),
(1002, 'visiontracker', '2024-11-08 09:30:00'),
(1003, 'torchscope',    '2025-01-01 08:15:00');

-- timestamp_project records project creation or activity
INSERT INTO timestamp_project VALUES
('torchscope',    '2024-09-22 18:45:00'),
('visiontracker', '2024-11-07 14:15:00');

"""
)


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
    "projects": [],
    "models": [],
    "runs": [],
    "line_plots": [],
    "dynamic_params": [
        {"name": "learning_rate", "value": 0.001, "min": 0.0001, "max": 0.01, "step": 0.0001},
        {"name": "batch_size", "value": 32, "min": 8, "max": 128, "step": 8},
        {"name": "num_epochs", "value": 10, "min": 1, "max": 100, "step": 1}
    ],
}


@app.get("/frontend/api/data")
def get_data():
    global selected_project, selected_model, selected_run
    # data["dynamic_params"] = []
    data["line_plots"] = []
    if "selected_project" not in data:
        data["projects"] = [
            row[0]
            for row in db_conn.execute(
                "SELECT DISTINCT project FROM timestamp_project"
            ).fetchall()
        ]
        return data
    elif "selected_model" not in data:
        data["models"] = [
            row[0]
            for row in db_conn.execute(
                f"""
            SELECT DISTINCT model FROM project_models
            WHERE project = '{data['selected_project']}'
        """
            ).fetchall()
        ]
        return data
    elif "selected_run" not in data:
        data["runs"] = [
            row[0]
            for row in db_conn.execute(
                f"""
            SELECT DISTINCT runs FROM model_runs
            WHERE model = {data['selected_model']}
        """
            ).fetchall()
        ]
    else:
        df = db_conn.execute(f"""SELECT * FROM run_{data['selected_run']}""").df()
        x_label = df.columns[0]
        y_labels = df.columns[1:]
        data["line_plots"] = [
            {"x": df[x_label].tolist(), "y": df[y].tolist(), "name": y}
            for y in y_labels
        ]

    return data


@app.post("/frontend/api/update-parameter")
def set_params(params: dict):
    print(params)
    for p in list(
        filter(lambda p: p["name"] == params["name"], data["dynamic_params"])
    ):
        p["value"] = params["value"]

    return {"status": "success", "message": "Parameters saved successfully"}


@app.post("/frontend/api/selected-instance")
def set_project(params: dict):
    match params["type"]:
        case "Projects":
            data["selected_project"] = params["selection"]
            data.pop("selected_model", None)
            data.pop("selected_run", None)
            data["models"] = []
            data["runs"] = []
        case "Models":
            data["selected_model"] = params["selection"]
            data.pop("selected_run", None)
            data["runs"] = []
        case "Runs":
            data["selected_run"] = params["selection"]
        case _:
            return {"status": "error", "message": "Invalid type"}
    return {"status": "success", "message": "Parameters saved successfully"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # data = await websocket.receive_text()
            # print("Received from client:", data)
            # await websocket.send_text(f"You said: {data}")
            await websocket.send_text(f"Server time: {time.time()}")
            await asyncio.sleep(1)
            data = await websocket.receive_text()
            print("Received from client:", data)
        except Exception as e:
            print("Client disconnected:", e)
            break

def run():
    uvicorn.run("torchscope.main:app", host="127.0.0.1", port=8000, reload=True)
