import torch
import torch.nn as nn
from torchscope.model.hashing import get_model_hash
from torchscope.model.graph import get_model_svg
import requests
from enum import Enum


class DataType(Enum): 
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "VARCHAR"

    def __str__(self):
        return self.value

    def _get_python_type(self): 
        if self == self.INTEGER:
            return int
        elif self == self.FLOAT:
            return float
        elif self == self.STRING:
            return str
        else:
            raise ValueError(f"Unsupported data type: {self.type}")

class DataPoint:
    def __init__(self, name: str, type: DataType):
        self.name = name
        self.type = type
        self.value = None

    def update(self, value):
        if isinstance(value, self.type._get_python_type()):
            self.value = value
            print(f"DataPoint '{self.name}' updated to {self.value} of type {self.type} {type(self.value).__name__}")
        else:
            raise TypeError(f"Value must be of type {self.type._get_python_type().__name__}")


class Scope: 
    def __init__(self, project_name: str, model: nn.Module): 
        self.project_name = project_name
        self.model = model
        self.svg = get_model_svg(model)
        self.model_hash = get_model_hash(model)
        self.registration_url = "http://127.0.0.1:8000/user/register"
        self.data_url = "http://127.0.0.1:8000/user/data"
        self.schema = {"iteration": "INTEGER"}
        self.data_points = {}

    def register(self, model_name: str = None): 
        data = {
            "model": self.model_hash,
            "project": self.project_name,
            "schema": self.schema,
            "svg": self.svg.decode("utf-8"),
        }
        print(data)
        if model_name:
            data["model_name"] = model_name
        response = requests.post(self.registration_url, json=data)
        if response.status_code == 200:
            response_data = response.json()
            print(f"Registration successful: {response_data}")
            self.run_id = response_data.get("run_id")
            return response_data.get("run_id")
        else:
            print(f"Registration failed: {response.text}")
            return None

    def get_data_handle(self, data_name: str, data_type: DataType):
        d = DataPoint(name=data_name, type=data_type)
        self.data_points[data_name] = d
        self.schema[data_name] = str(data_type)
        return d

    def _register_data(self, data: list):
        payload = {
            "run_id": self.run_id,
            "data": data
        }
        response = requests.post(self.data_url, json=payload)
        if response.status_code == 200:
            print("Data registered successfully")
        else:
            print(f"Failed to register data: {response.text}")

    def update(self, iteration: int): 
        data = {"iteration": iteration}
        for name, point in self.data_points.items():
            if point.value is not None:
                data[name] = point.value
        if data:
            print(f"Updating data for iteration {iteration}: {data}")
            self._register_data([data])
        else:
            print("No data to register")

