class Watcher: 
    def __init__(self, var_lambda): 
        self.var_lambda = var_lambda

    def print(self):
        print(f"Watcher: {self.var_lambda()}")


a = 10 
watcher = Watcher(lambda: a)
watcher.print()
a = 20
watcher.print()
