from torch.fx import symbolic_trace
from hashlib import md5


def hash_layers(model):
    hash = 0
    for layer in model.children():
        hash += int(md5(str(layer).encode()).hexdigest(), 16)
    return hash


def hash_graph(model):
    traced_model = symbolic_trace(model)
    graph_hash = md5(str(traced_model.graph).encode()).hexdigest()
    return int(graph_hash, 16)


def get_model_hash(model):
    layer_hash = hash_layers(model)
    graph_hash = hash_graph(model)
    return hex(graph_hash + layer_hash)
