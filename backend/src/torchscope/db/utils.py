import duckdb as db 
import pandas as pd


def drop_run(db_conn, run_id):
    db_conn.execute(f"DROP TABLE IF EXISTS run_{run_id};")

def drop_project_models(db_conn):
    db_conn.execute("DROP TABLE IF EXISTS project_models;")

def drop_model_runs(db_conn): 
    db_conn.execute("DROP TABLE IF EXISTS model_runs;")

def drop_timestamp_project(db_conn): 
    db_conn.execute("DROP TABLE IF EXISTS timestamp_project;")

def create_run_table(db_conn, run_id: int, columns: dict):
    column_definitions = ""
    for column_name, column_type in columns.items():
        if column_definitions:
            column_definitions += ", "
        column_definitions += f"{column_name} {column_type}"
    db_conn.execute(f"CREATE TABLE IF NOT EXISTS run_{run_id} ({column_definitions});")

def create_model_runs_table(db_conn): 
    db_conn.execute(
        """
        CREATE TABLE IF NOT EXISTS model_runs (
            runs      VARCHAR,
            run_name  VARCHAR,
            model     VARCHAR,
            timestamp TIMESTAMP
        );
        """
    )

def create_project_models_table(db_conn): 
    db_conn.execute(
        """
        CREATE TABLE IF NOT EXISTS project_models (
            model     VARCHAR,
            model_name  VARCHAR,
            project   VARCHAR,
            timestamp TIMESTAMP
        );
        """
    )

def create_timestamp_project_table(db_conn): 
    db_conn.execute(
        """
        CREATE TABLE IF NOT EXISTS timestamp_project (
            project   VARCHAR,
            timestamp TIMESTAMP
        );
        """
    )

def insert_run_data(db_conn, run_id: int, data: list):
    try: 
        # get the column names from the first row of data from database 1
        fields = db_conn.execute(f"PRAGMA table_info(run_{run_id});").fetchdf()['name'].tolist()
        for sample in data: 
            data = []
            for field in fields: 
                if field in sample:
                    data.append(sample[field])
                else:
                    raise ValueError(f"Field {field} not found in sample data")
            db_conn.execute(f"INSERT INTO run_{run_id} VALUES ({', '.join(['?'] * len(data))});", data)
                

        

    except Exception as e: 
        print(f"Error fetching schema info for run_{run_id}: {e}")
        return


def insert_model_run(db_conn, run_id: int, run_name: str, model_id: int):
    try:
        db_conn.execute(
            "INSERT INTO model_runs (runs, run_name, model, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP);",
            (run_id, run_name, model_id)
        )
    except Exception as e:
        print(f"Error inserting model run: {e}")
        return

def insert_project_model(db_conn, model_id: int, model_name: str, project: str): 
    try:
         # Ensure the table exists before inserting
        db_conn.execute(
            "INSERT INTO project_models (model, model_name, project, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP);",
            (model_id, model_name, project)
        )
    except Exception as e:
        print(f"Error inserting project model: {e}")
        return

def insert_timestamp_project(db_conn, project: str): 
    try:
        db_conn.execute(
            "INSERT INTO timestamp_project (project, timestamp) VALUES (?, CURRENT_TIMESTAMP);",
            (project,)
        )
    except Exception as e:
        print(f"Error inserting timestamp project: {e}")
        return
