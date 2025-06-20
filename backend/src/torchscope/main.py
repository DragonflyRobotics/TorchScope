from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketState
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import duckdb as db
import asyncio

from torchscope.db.utils import (
    drop_run,
    drop_project_models,
    drop_model_runs,
    drop_timestamp_project,
    insert_run_data,
    get_svg_from_model,
)
from torchscope.db.basic import (
    new_project,
    new_model_session,
    new_run_session,
    get_runs_from_model_ord,
    get_models_from_project_ord,
    get_charts,
    get_projects_ord,
)


new_data_event = asyncio.Event()
new_session_event = asyncio.Event()

dynamic_params = {}

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




@app.post("/user/register")
def register_user(info: dict):
    model = info["model"]
    try:
        model_name = info["model_name"]
    except KeyError:
        model_name = ""
    project = info["project"]
    schema = info["schema"]
    svg = info["svg"]
    with db.connect("torchscope.db") as db_conn:
        if project not in get_projects_ord(db_conn):
            print(f"Creating new project: {project}")
            new_project(db_conn, project)

        if model not in get_models_from_project_ord(db_conn, project, "model"):
            print(f"Creating new model session: {model}")
            if len(model_name) > 0:
                new_model_session(db_conn, model, project, svg, model_name=model_name)
                print(f"Creating new run session: {model} - {model_name}")
            else:
                new_model_session(db_conn, model, project, svg)
        else:
            print(f"Model {model} already exists in project {project}")
        r_id = new_run_session(db_conn, model, schema)
        new_session_event.set()  # Trigger new session event for websocket clients

    return {
        "status": "success",
        "message": "Registered successfully",
        "model": model,
        "project": project,
        "run_id": r_id,
    }


@app.post("/user/data")
def register_data(data: dict):
    run_id = data["run_id"]
    data = data["data"]
    # print(f"Registering data for run {run_id}: {data}")
    with db.connect("torchscope.db") as db_conn:
        try:
            insert_run_data(db_conn, run_id, data)
            new_data_event.set()  # Trigger data update for websocket clients
        except Exception as e:
            print(f"Error inserting data: {e}")
            return {"status": "error", "message": str(e)}
    return {"status": "success", "message": "Data registered successfully"}
    


@app.get("/frontend/api/projects")
def get_projects():
    with db.connect("torchscope.db") as db_conn:
        return get_projects_ord(db_conn)


@app.post("/frontend/api/models")
def get_models(project: dict):
    print(f"Fetching models for project: {project}")
    with db.connect("torchscope.db") as db_conn:
        model_names = get_models_from_project_ord(
            db_conn, project["project"], "model_name"
        )
        model_ids = get_models_from_project_ord(db_conn, project["project"], "model")
        return [
            {"model": model_id, "name": model_name}
            for model_id, model_name in zip(model_ids, model_names)
        ]


@app.post("/frontend/api/runs")
def get_models(model: dict):
    print(f"Fetching run for project: {model}")
    with db.connect("torchscope.db") as db_conn:
        run_names = get_runs_from_model_ord(db_conn, model["model"], "run_name")
        run_ids = get_runs_from_model_ord(db_conn, model["model"], "runs")
        return {
            "svg": get_svg_from_model(db_conn, model["model"]),
            "runs": [
                {"run": run_id, "name": run_name}
                for run_id, run_name in zip(run_ids, run_names)
            ],
        }


@app.post("/frontend/api/update-parameter")
def set_params(params: dict, client_id: str):
    global dynamic_params
    print(f"Setting parameters for client {client_id}: {params}")
    dynamic_params[client_id] = params["dynamic_params"]
    new_data_event.set()  # Trigger data update for websocket clients
    # for p in list(
    #     filter(lambda p: p["name"] == params["name"], data["dynamic_params"])
    # ):
    #     p["value"] = params["value"]


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


async def wait_for_new_session_event():
    await new_session_event.wait()
    return ("new_session", [])


current_run = {}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    global current_run, dynamic_params
    await websocket.accept()
    current_run[client_id] = None
    while websocket.client_state == WebSocketState.CONNECTED:
        try:
            done, pending = await asyncio.wait(
                [
                    asyncio.create_task(wait_for_client(websocket)),
                    asyncio.create_task(wait_for_data_event()),
                    asyncio.create_task(wait_for_new_session_event()),
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
                            current_run[client_id] = None
                        else:
                            current_run[client_id] = data["run"]
                            print(f"Selected run: {current_run}")
                        new_data_event.set()  # Trigger data update
                elif source == "event":
                    print("Data event triggered, updating graph")
                    data = {}
                    if current_run[client_id] is not None:
                        with db.connect("torchscope.db") as db_conn:
                            # df = db_conn.execute(
                            #     f"""SELECT * FROM run_{current_run}"""
                            # ).df()
                            df = get_charts(db_conn, current_run[client_id])
                        print("does it work", dynamic_params)
                        print("my id", client_id)
                        x_label = df.columns[0]
                        y_labels = df.columns[1:]
                        if dynamic_params.get(client_id) and len(list(filter(lambda p: p.get('name') == 'smoothing', dynamic_params.get(client_id)))) > 0:
                            print("Smoothing parameter found")
                            smoothing = list(filter(lambda p: p.get('name') == 'smoothing', dynamic_params[client_id]))[0].get('value')
                            for y_name in y_labels:
                                y = df[y_name]
                                new_y = [y[0]]
                                for i in range(1, len(y)):
                                    new_y.append(
                                        (new_y[-1] * smoothing) + (y[i] * (1 - smoothing))
                                    )
                                df[y_name] = new_y
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
                elif source == "new_session":
                    await websocket.send_json(
                        {
                            "type": "new_session",
                            "data": {},
                        }
                    )
                    new_session_event.clear()

            # Cancel any pending tasks to avoid memory leaks
            for task in pending:
                task.cancel()

        except Exception as e:
            print("Client disconnected:", e)
            break


def run():
    uvicorn.run("torchscope.main:app", host="127.0.0.1", port=8000, reload=False)
