
# with db.connect("torchscope.db") as db_conn:
#     drop_run(db_conn, 3821)
#     drop_run(db_conn, 4141)
#     drop_run(db_conn, 3912)
#     drop_run(db_conn, 4829)
#     drop_project_models(db_conn)
#     drop_model_runs(db_conn)
#     drop_timestamp_project(db_conn)
#     new_project(db_conn, "torchscope")
#     new_project(db_conn, "visiontracker")
#     m1001 = new_model_session(db_conn, "torchscope")
#     m1002 = new_model_session(db_conn, "visiontracker")
#     m1003 = new_model_session(db_conn, "torchscope")
#     r3821 = new_run_session(
#         db_conn,
#         m1001,
#         {
#             "iteration": "INTEGER",
#             "lr": "FLOAT",
#             "loss": "FLOAT",
#             "accuracy": "FLOAT",
#             "val_loss": "FLOAT",
#         },
#     )
#     r4141 = new_run_session(
#         db_conn,
#         m1001,
#         {
#             "iteration": "INTEGER",
#             "lr": "FLOAT",
#             "loss": "FLOAT",
#             "accuracy": "FLOAT",
#         },
#     )
#     r3912 = new_run_session(
#         db_conn,
#         m1002,
#         {
#             "iteration": "INTEGER",
#             "lr": "FLOAT",
#             "loss": "FLOAT",
#         },
#     )
#     r4829 = new_run_session(
#         db_conn,
#         m1003,
#         {
#             "iteration": "INTEGER",
#             "lr": "FLOAT",
#         },
#     )
#     insert_run_data(
#         db_conn,
#         r3821,
#         [
#             {
#                 "iteration": 1,
#                 "lr": 0.01,
#                 "loss": 0.693,
#                 "accuracy": 0.50,
#                 "val_loss": 0.700,
#             },
#             {
#                 "iteration": 2,
#                 "lr": 0.01,
#                 "loss": 0.682,
#                 "accuracy": 0.55,
#                 "val_loss": 0.690,
#             },
#             {
#                 "iteration": 3,
#                 "lr": 0.01,
#                 "loss": 0.670,
#                 "accuracy": 0.60,
#                 "val_loss": 0.675,
#             },
#         ],
#     )
#     insert_run_data(
#         db_conn,
#         r4141,
#         [
#             {"iteration": 1, "lr": 0.01, "loss": 0.693, "accuracy": 0.50},
#             {"iteration": 2, "lr": 0.01, "loss": 0.682, "accuracy": 0.55},
#             {"iteration": 3, "lr": 0.01, "loss": 0.670, "accuracy": 0.60},
#         ],
#     )
#
#     insert_run_data(
#         db_conn,
#         r3912,
#         [
#             {"iteration": 1, "lr": 0.01, "loss": 0.695},
#             {"iteration": 2, "lr": 0.01, "loss": 0.688},
#             {"iteration": 3, "lr": 0.01, "loss": 0.673},
#         ],
#     )
#
#     insert_run_data(
#         db_conn,
#         r4829,
#         [
#             {"iteration": 1, "lr": 0.005},
#             {"iteration": 2, "lr": 0.005},
#             {"iteration": 3, "lr": 0.005},
#         ],
#     )
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(update_data())
