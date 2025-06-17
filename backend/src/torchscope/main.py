from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketState
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import duckdb as db
import asyncio

from torchscope.db.utils import *
from torchscope.db.basic import *


new_data_event = asyncio.Event()

with db.connect("torchscope.db") as db_conn:
    drop_run(db_conn, 3821)
    drop_run(db_conn, 4141)
    drop_run(db_conn, 3912)
    drop_run(db_conn, 4829)
    drop_project_models(db_conn)
    drop_model_runs(db_conn)
    drop_timestamp_project(db_conn)
    new_project(db_conn, "torchscope")
    new_project(db_conn, "visiontracker")
    m1001 = new_model_session(db_conn, "torchscope")
    m1002 = new_model_session(db_conn, "visiontracker")
    m1003 = new_model_session(db_conn, "torchscope")
    r3821 = new_run_session(db_conn, m1001, {
                            "iteration": "INTEGER",
                            "lr": "FLOAT",
                            "loss": "FLOAT",
                            "accuracy": "FLOAT",
                            "val_loss": "FLOAT",
                            })
    r4141 = new_run_session(db_conn, m1001, {
                            "iteration": "INTEGER",
                            "lr": "FLOAT",
                            "loss": "FLOAT",
                            "accuracy": "FLOAT",
                            })
    r3912 = new_run_session(db_conn, m1002, {
                            "iteration": "INTEGER",
                            "lr": "FLOAT",
                            "loss": "FLOAT",
                            })
    r4829 = new_run_session(db_conn, m1003, {
                            "iteration": "INTEGER",
                            "lr": "FLOAT",
                            })
    insert_run_data(
        db_conn,
        r3821,
        [
            {
                "iteration": 1,
                "lr": 0.01,
                "loss": 0.693,
                "accuracy": 0.50,
                "val_loss": 0.700,
            },
            {
                "iteration": 2,
                "lr": 0.01,
                "loss": 0.682,
                "accuracy": 0.55,
                "val_loss": 0.690,
            },
            {
                "iteration": 3,
                "lr": 0.01,
                "loss": 0.670,
                "accuracy": 0.60,
                "val_loss": 0.675,
            },
        ],
    )
    insert_run_data(
        db_conn,
        r4141,
        [
            {"iteration": 1, "lr": 0.01, "loss": 0.693, "accuracy": 0.50},
            {"iteration": 2, "lr": 0.01, "loss": 0.682, "accuracy": 0.55},
            {"iteration": 3, "lr": 0.01, "loss": 0.670, "accuracy": 0.60},
        ],
    )

    insert_run_data(
        db_conn,
        r3912,
        [
            {"iteration": 1, "lr": 0.01, "loss": 0.695},
            {"iteration": 2, "lr": 0.01, "loss": 0.688},
            {"iteration": 3, "lr": 0.01, "loss": 0.673},
        ],
    )

    insert_run_data(
        db_conn,
        r4829,
        [
            {"iteration": 1, "lr": 0.005},
            {"iteration": 2, "lr": 0.005},
            {"iteration": 3, "lr": 0.005},
        ],
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


current_hash = None


@app.get("/frontend/api/projects")
def get_projects():
    with db.connect("torchscope.db") as db_conn:
        return [
            row[0]
            for row in db_conn.execute(
                "SELECT DISTINCT project FROM timestamp_project ORDER BY timestamp ASC"
            ).fetchall()
        ]


@app.post("/frontend/api/models")
def get_models(project: dict):
    print(f"Fetching models for project: {project}")
    with db.connect("torchscope.db") as db_conn:
        model_names =  [
            row[0]
            for row in db_conn.execute(
                f"""
            SELECT DISTINCT model_name FROM project_models
            WHERE project = '{project['project']}'
            ORDER BY timestamp ASC
        """
            ).fetchall()
        ]
        model_ids =  [
            row[0]
            for row in db_conn.execute(
                f"""
            SELECT DISTINCT model FROM project_models
            WHERE project = '{project['project']}'
            ORDER BY timestamp ASC
        """
            ).fetchall()
        ]
        return [{"model": model_id, "name": model_name}
            for model_id, model_name in zip(model_ids, model_names)
        ]


@app.post("/frontend/api/runs")
def get_models(model: dict):
    print(f"Fetching run for project: {model}")
    with db.connect("torchscope.db") as db_conn:
        run_names = [
            row[0]
            for row in db_conn.execute(
                f"""
            SELECT DISTINCT run_name FROM model_runs
            WHERE model = '{model['model']}'
            ORDER BY timestamp ASC 
        """
            ).fetchall()
        ]
        run_ids = [
            row[0]
            for row in db_conn.execute(
                f"""
            SELECT DISTINCT runs FROM model_runs
            WHERE model = '{model['model']}'
            ORDER BY timestamp ASC 
        """
            ).fetchall()
        ]
        return [{"run": run_id, "name": run_name}
            for run_id, run_name in zip(run_ids, run_names)
        ]


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
                    asyncio.create_task(wait_for_data_event()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
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
                            print(f"Selected run: {current_run}")
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
