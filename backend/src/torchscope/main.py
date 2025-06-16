from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketState
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import duckdb as db
import asyncio

from torchscope.db.utils import drop_run


new_data_event = asyncio.Event()

with db.connect("torchscope.db") as db_conn:
    drop_run(db_conn, 3821)
    drop_run(db_conn, 4141)
    drop_run(db_conn, 3912)
    drop_run(db_conn, 4829)

with db.connect("torchscope.db") as db_conn:
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


# data = {
#     "projects": [],
#     "models": [],
#     "runs": [],
#     "dynamic_params": [
#         {
#             "name": "learning_rate",
#             "value": 0.001,
#             "min": 0.0001,
#             "max": 0.01,
#             "step": 0.0001,
#         },
#         {"name": "batch_size", "value": 32, "min": 8, "max": 128, "step": 8},
#         {"name": "num_epochs", "value": 10, "min": 1, "max": 100, "step": 1},
#     ],
# }

current_hash = None

@app.get("/frontend/api/projects")
def get_projects(): 
    with db.connect("torchscope.db") as db_conn:
        return [row[0] for row in db_conn.execute("SELECT DISTINCT project FROM timestamp_project").fetchall()]

@app.post("/frontend/api/models")
def get_models(project: dict): 
    print(f"Fetching models for project: {project}")
    with db.connect("torchscope.db") as db_conn:
        return [row[0] for row in db_conn.execute(
            f"""
            SELECT DISTINCT model FROM project_models
            WHERE project = '{project['project']}'
        """
        ).fetchall()]

@app.post("/frontend/api/runs")
def get_models(model: dict): 
    print(f"Fetching run for project: {model}")
    with db.connect("torchscope.db") as db_conn:
        return [row[0] for row in db_conn.execute(
            f"""
            SELECT DISTINCT runs FROM model_runs 
            WHERE model = '{model['model']}'
        """
        ).fetchall()]


@app.post("/frontend/api/update-parameter")
def set_params(params: dict):
    print(params)
    # for p in list(
    #     filter(lambda p: p["name"] == params["name"], data["dynamic_params"])
    # ):
    #     p["value"] = params["value"]




# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(update_data())


current_run = None
async def update_data():
    global current_run 
    while True:
        await asyncio.sleep(3)  # Adjust the interval as needed
        if current_run is not None:
            print(f"Updating data for run {current_run}")
            with db.connect("torchscope.db") as db_conn:
                df = db_conn.execute(f"""SELECT * FROM run_{current_run}""").df()
            x_label = df.columns[0]
            y_labels = df.columns[1:]
            new_row = {x_label: df[x_label].iloc[-1] + 1}
            for y in y_labels:
                new_row[y] = df[y].iloc[-1] + 1

            df.loc[len(df)] = new_row  # only use with a RangeIndex!
            with db.connect("torchscope.db") as db_conn:
                db_conn.execute(
                    f"""INSERT INTO run_{current_run} VALUES ({', '.join(map(str, new_row.values()))})"""
                )
            new_data_event.set()
    return {"status": "success", "message": "Parameters saved successfully"}



async def wait_for_client(websocket):
    msg = await websocket.receive_json()
    return ("client", msg)

async def wait_for_data_event():
    await new_data_event.wait()
    return ("event", []) 

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # current_run = None
    global current_run
    await websocket.accept()
    while websocket.client_state == WebSocketState.CONNECTED:
        try:
            done, pending = await asyncio.wait(
                [
                    asyncio.create_task(wait_for_client(websocket)),
                    asyncio.create_task(wait_for_data_event())
                ],
                return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                print(task)
                source, data = task.result()
                if source == "client":
                    if data["type"] == "selected_run":
                        if data["run"] == "null": 
                            print("No run selected, clearing current_run")
                            current_run = None
                        else:
                            current_run = data["run"]
                        new_data_event.set()  # Trigger data update
                elif source == "event": 
                    print("Data event triggered, updating graph")
                    data = {}
                    if current_run is not None:
                        with db.connect("torchscope.db") as db_conn:
                            df = db_conn.execute(
                                f"""SELECT * FROM run_{current_run}"""
                            ).df()
                        x_label = df.columns[0]
                        y_labels = df.columns[1:]
                        data["line_plots"] = [
                            {"x": df[x_label].tolist(), "y": df[y].tolist(), "name": y}
                            for y in y_labels
                        ]
                        await websocket.send_json(
                            {
                                "type": "update_graph",
                                "data": data["line_plots"],
                            }
                        )
                    else:
                        await websocket.send_json(
                            {
                                "type": "no_data",
                            }
                        )
                    new_data_event.clear()
            # Cancel any pending tasks to avoid memory leaks
            for task in pending:
                task.cancel()

        except Exception as e:
            print("Client disconnected:", e)
            break


def run():
    uvicorn.run("torchscope.main:app", host="127.0.0.1", port=8000, reload=False)
