

class ModelRegistry:
    def __init__(self):
        self.models = {}
        self.results = {}

    def register(self, name, model):
        self.models[name] = model

    def evaluate(self, series, backtest_fn, **bt_kwargs):
        for name, model in self.models.items():
            result = backtest_fn(series, model, **bt_kwargs)
            self.results[name] = result

    def best_model(self, metric="avg_rmse"):
        return min(self.results.items(), key=lambda x: x[1][metric])



