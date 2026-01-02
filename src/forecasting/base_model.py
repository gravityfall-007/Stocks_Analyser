from abc import ABC, abstractmethod
import pandas as pd

class BaseForecaster(ABC):
    def __init__(self, config: dict = {}):
        self.config = config

    @abstractmethod
    def fit(self, series: pd.Series, **kwargs):
        pass

    @abstractmethod
    def forecast(self, steps: int, **kwargs) -> pd.Series:
        pass
