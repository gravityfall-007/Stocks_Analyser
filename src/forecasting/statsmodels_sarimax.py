
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from .base_model import BaseForecaster

class StatsmodelsSARIMAX(BaseForecaster):
    def __init__(self, order=(1,1,1), seasonal_order=(1,1,1,12), exog=None):
        super().__init__()
        self.order = order
        self.seasonal_order = seasonal_order
        self.exog = exog
        self.model = None

    def fit(self, series: pd.Series, exog=None):
        if hasattr(series.index, 'freq') and series.index.freq is None:
            series.index.freq = pd.infer_freq(series.index)
            
        self.model = SARIMAX(series, 
                             exog=exog if exog is not None else self.exog,
                             order=self.order,
                             seasonal_order=self.seasonal_order).fit(disp=False)
        return self

    def forecast(self, steps: int, exog=None) -> pd.Series:
        return self.model.get_forecast(steps=steps, exog=exog).predicted_mean
