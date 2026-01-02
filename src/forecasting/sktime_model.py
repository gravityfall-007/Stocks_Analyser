import pandas as pd
from sktime.forecasting.compose import make_reduction
from sklearn.ensemble import RandomForestRegressor
from .base_model import BaseForecaster

class SKTimeML(BaseForecaster):
    def __init__(self, model=None):
        super().__init__()
        self.model = model or RandomForestRegressor(n_estimators=100)
        self.forecaster = None

    def fit(self, series: pd.Series, X_train=None):
        self.forecaster = make_reduction(self.model, strategy="recursive")
        self.forecaster.fit(series, X=X_train)
        return self

    def forecast(self, steps: int, X_future=None) -> pd.Series:
        # `fh` = forecast horizon sequence
        fh = list(range(1, steps+1))
        y_pred = self.forecaster.predict(fh=fh, X=X_future)
        return pd.Series(y_pred, index=range(len(y_pred)))
