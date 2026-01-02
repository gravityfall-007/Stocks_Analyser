import pandas as pd
from tbats import TBATS
from .base_model import BaseForecaster

class TBATSForecaster(BaseForecaster):
    def __init__(self, seasonal_periods=(5, 20, 252)):
        # 5-- Trading week
        # 20-- Trading month
        # 252-- Trading year
        super().__init__()
        self.estimator = TBATS(
            seasonal_periods=seasonal_periods,
            use_arma_errors=True,
            use_box_cox=False
        )
        self.model = None

    def fit(self, series: pd.Series):
        self.model = self.estimator.fit(series.values)
        return self

    def forecast(self, steps: int) -> pd.Series:
        forecast = self.model.forecast(steps)
        return pd.Series(forecast)
