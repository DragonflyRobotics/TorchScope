import duckdb as db 


def drop_run(db_conn, run_id):
    db_conn.execute(f"DROP TABLE IF EXISTS run_{run_id};")

