import torch
import torch.nn as nn
from torchscope.model.hashing import get_model_hash

class Scope: 
    def __init__(self, project_name: str, model: nn.Module): 
        self.project_name = project_name
        self.model = model
        self.model_hash = get_model_hash(model)
