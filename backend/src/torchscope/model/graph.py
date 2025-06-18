from torch.fx import passes, symbolic_trace

def get_model_svg(model):
    traced_model = symbolic_trace(model)
    g = passes.graph_drawer.FxGraphDrawer(traced_model, model.__class__.__name__)
    return g.get_dot_graph().create_svg()
