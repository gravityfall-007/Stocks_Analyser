import pandas as pd
from darts import TimeSeries
from darts.models import NBEATSModel
from .base_model import BaseForecaster

class DartsNBEATS(BaseForecaster):
    def __init__(self, input_chunk=30, output_chunk=10, **kwargs):
        super().__init__(kwargs)
        self.model = NBEATSModel(input_chunk_length=input_chunk,
                                  output_chunk_length=output_chunk,
                                  **kwargs)

    def fit(self, series: pd.Series, **kwargs):
        ts = TimeSeries.from_series(series)
        self.model.fit(ts, verbose=False)
        return self

    def forecast(self, steps: int, **kwargs) -> pd.Series:
        forecast_ts = self.model.predict(n=steps)
        return forecast_ts.pd_series()
