import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from .base_model import BaseForecaster

class StatsmodelsETS(BaseForecaster):
    def __init__(self, trend="add", seasonal="add", seasonal_periods=12):
        super().__init__()
        self.trend = trend
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        self.model = None
        self.fitted = None

    def fit(self, series: pd.Series):
        if hasattr(series.index, 'freq') and series.index.freq is None:
            series.index.freq = pd.infer_freq(series.index)

        self.model = ExponentialSmoothing(
            series,
            trend=self.trend,
            seasonal=self.seasonal,
            seasonal_periods=self.seasonal_periods
        )
        self.fitted = self.model.fit()
        return self

    def forecast(self, steps: int) -> pd.Series:
        return self.fitted.forecast(steps)
