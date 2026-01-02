import pandas as pd
from gluonts.dataset.common import ListDataset
from gluonts.mx.model.deepar import DeepAREstimator
from gluonts.mx.trainer import Trainer
from .base_model import BaseForecaster

class GluonTSDeepAR(BaseForecaster):
    def __init__(self, freq="D", pred_len=14, **kwargs):
        super().__init__(kwargs)
        self.estimator = DeepAREstimator(freq=freq,
                                         prediction_length=pred_len,
                                         trainer=Trainer(**kwargs))
        self.predictor = None

    def fit(self, series: pd.Series, start=None):
        train_dataset = ListDataset([{"start": start, "target": series.values}], freq=self.estimator.freq)
        self.predictor = self.estimator.train(train_dataset)
        return self

    def forecast(self, steps: int, **kwargs) -> pd.DataFrame:
        forecast_it = self.predictor.predict(
            ListDataset([{"start": None, "target": []}], freq=self.estimator.freq)
        )
        return pd.Series(list(next(forecast_it).mean)[:steps])
