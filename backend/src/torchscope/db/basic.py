from torchscope.db.utils import *
import uuid


def new_run_session(db_conn, model_id, columns: dict, run_name=None):
    run_id = str(uuid.uuid4()).replace("-", "_")
    create_run_table(db_conn, run_id, columns)
    result = db_conn.execute(
        f"""
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_name = 'model_runs'
    """
    ).fetchone()[0]
    if result == 0:
        print("Creating model_runs table as it does not exist.")
        create_model_runs_table(db_conn)

    existing_runs = [
        row[0]
        for row in db_conn.execute(
            f""" SELECT DISTINCT runs FROM model_runs WHERE model = '{model_id}' """
        ).fetchall()
    ]
    print(f"Existing runs for model {model_id}: {existing_runs}")
    if run_name is None:
        name = f"Run_{len(existing_runs) + 1}"
        print(f"Creating new run with name: {name}")
    insert_model_run(db_conn, run_id, name, model_id)
    return run_id


def new_model_session(db_conn, project_name, model_name=None):
    model_id = str(uuid.uuid4()).replace("-", "_")
    result = db_conn.execute(
        f"""
            SELECT COUNT(*)
                FROM information_schema.tables
        WHERE table_name = 'project_models'
            """
    ).fetchone()[0]
    if result == 0:
        print("Creating project_models table as it does not exist.")
        create_project_models_table(db_conn)
    existing_models = [
        row[0]
        for row in db_conn.execute(
            f""" SELECT DISTINCT model FROM project_models WHERE project = '{project_name}' """
        ).fetchall()
    ]
    if model_name is None:
        name = f"Model_{len(existing_models) + 1}"
        print(f"Creating new model with name: {name}")
    else:
        name = model_name
    insert_project_model(db_conn, model_id, name, project_name)
    insert_timestamp_project(db_conn, project_name)
    return model_id


def new_project(db_conn, project_name):
    result = db_conn.execute(
        f"""
        SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = 'timestamp_project'
        """
    ).fetchone()[0]
    if result == 0:
        create_timestamp_project_table(db_conn)
    insert_timestamp_project(db_conn, project_name)
    return project_name


def get_charts(db_conn, run_id: str):
    try:
        return db_conn.execute(f"""SELECT * FROM run_{run_id}""").df()
    except Exception as e:
        print(f"Error fetching charts for run {run_id}: {e}")
        return []


def get_runs_from_model_ord(db_conn, model_id: str, col_name: str):
    try:
        return [
            row[0]
            for row in db_conn.execute(
                f"""
            SELECT DISTINCT {col_name} FROM model_runs
            WHERE model = '{model_id}'
            ORDER BY timestamp ASC
        """
            ).fetchall()
        ]
    except Exception as e:
        print(f"Error fetching runs for model {model_id}: {e}")
        return []


def get_models_from_project_ord(db_conn, project_name: str, col_name: str):
    try:
        return [
            row[0]
            for row in db_conn.execute(
                f"""
            SELECT DISTINCT {col_name} FROM project_models
            WHERE project = '{project_name}'
            ORDER BY timestamp ASC
        """
            ).fetchall()
        ]
    except Exception as e:
        print(f"Error fetching models for project {project_name}: {e}")
        return []
