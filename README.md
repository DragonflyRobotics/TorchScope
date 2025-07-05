# TorchScope
A blazing fast 🔥, super charged🔋 Tensorboard alternative with self-hosted backend and dynamic model version history.

![Screenshot](https://github.com/DragonflyRobotics/TorchScope/blob/main/dash_ss.png)

## Features
* Dynamic live-updating graphs
* Fully adjustable grid for custom training dashboards
* **On-the-fly hyperparameter adjustment (LR, Patience, e. Finally tc)**
* **Fire and forget - Automatically tracks changes in model architecture and runs to create full revision history and run tracking**
* Flexible, Tensorboard-like API
* Database and self-hostable
* Saves model architecture for future reference.

## Premise
We have all been there, accidentally keeping the same log dir in Tensorboard and wiping all your other runs or forgetting which model variation produced those awesome results. Maybe your LR decay was too aggressive and you want to bump up the LR after 500 long epochs. With TorchScope, you can! TorchScope automatically tracks runs and model versions. All you need to do is tell it a project name and pass the model class. If the model architecture changed, it will create a new model tab automatically and reset the run count to 1. If no model change was detected, the run count will be incremented. All previous runs and models are stored for future reference. This is in addition to most features Tensorboard currently offers. Training has never been easier.

## Usage
**Note: This project is still experimental and doesn't guarantee functionality. Nevertheless, I appreciate any users, improvements, suggestions, and failures!**

Firstly, install all the dependencies in `backend/pyproject.toml` and `frontend/package.json` with their respective package managers. 

Here is how to do this with `uv` and `npm`:
```bash
In backend: uv sync
In frontend: npm i
```

Then, source the python environment (usually `source backend/.venv/bin/activate`) and start it with `uvicorn torchscope.main:app --host 127.0.0.1 --port 8000`. Then start the frontend with `node_modules/vite/bin/vite.js`.

Finally, install the torchscope library (yielded by `uv build`) in your project and follow the format in [example.py](https://github.com/DragonflyRobotics/TorchScope/blob/main/example.py) to loop into the TorchScope instance and start training.

The user experience is very much not seamless or professional yet. As the project develops, this experience will improve to match the ease-of-use of Tensorboard!
