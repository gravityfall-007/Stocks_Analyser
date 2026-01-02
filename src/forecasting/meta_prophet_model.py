import pandas as pd
from prophet import Prophet
from .base_model import BaseForecaster

class ProphetForecaster(BaseForecaster):
    def __init__(self, yearly=True, weekly=True, daily=False, **kwargs):
        super().__init__(kwargs)
        self.model = Prophet(
            yearly_seasonality=yearly,
            weekly_seasonality=weekly,
            daily_seasonality=daily,
            **kwargs
        )

    def fit(self, series: pd.Series):
        df = series.reset_index()
        df.columns = ["ds", "y"]
        self.model.fit(df)
        return self

    def forecast(self, steps: int) -> pd.Series:
        future = self.model.make_future_dataframe(periods=steps)
        forecast = self.model.predict(future)
        return forecast.tail(steps).set_index("ds")["yhat"]
