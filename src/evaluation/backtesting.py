import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def walk_forward_validation(
    series: pd.Series,
    model,
    train_size: int,
    horizon: int,
    step: int = 1
):
    """
    Generic walk-forward validation
    """
    metrics = []
    forecasts = []

    for start in range(train_size, len(series) - horizon, step):
        train = series.iloc[:start]
        test = series.iloc[start:start + horizon]

        model.fit(train)
        preds = model.forecast(horizon)

        mae = mean_absolute_error(test, preds)
        rmse = mean_squared_error(test, preds)

        metrics.append({"mae": mae, "rmse": rmse})
        forecasts.append(preds)

    return {
        "metrics": pd.DataFrame(metrics),
        "avg_mae": np.mean([m["mae"] for m in metrics]),
        "avg_rmse": np.mean([m["rmse"] for m in metrics]),
        "forecasts": forecasts
    }