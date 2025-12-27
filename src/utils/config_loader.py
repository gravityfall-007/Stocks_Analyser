import yaml

def load_stocks_config(path="config/stocks.yaml"):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("stocks", [])
