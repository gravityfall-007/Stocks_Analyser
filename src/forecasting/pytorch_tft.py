import pandas as pd
import torch
from pytorch_forecasting import TemporalFusionTransformer, TimeSeriesDataSet
from pytorch_forecasting.data import GroupNormalizer
from torch.utils.data import DataLoader
from .base_model import BaseForecaster

class PyTorchTFT(BaseForecaster):
    def __init__(self, config):
        super().__init__(config)
        self.model = None
        self.dataset = None

    def fit(self, series: pd.DataFrame, config=None):
        """
        Expect df with columns ["time_idx", "value", "group"]
        """
        config = config or self.config
        self.dataset = TimeSeriesDataSet(
            series,
            time_idx="time_idx",
            target="value",
            group_ids=["group"],
            min_encoder_length=config["min_enc"],
            max_encoder_length=config["max_enc"],
            min_prediction_length=config["min_pred"],
            max_prediction_length=config["max_pred"],
            target_normalizer=GroupNormalizer()
        )

        train_dl = DataLoader(self.dataset, batch_size=config.get("batch_size", 16), shuffle=True)
        self.model = TemporalFusionTransformer.from_dataset(
            self.dataset, 
            learning_rate=config.get("lr", 1e-3),
            hidden_size=config.get("hidden_size", 16),
        )

        self.model.fit(train_dl, max_epochs=config.get("epochs", 10))
        return self

    def forecast(self, val_dl: DataLoader) -> pd.Series:
        predictions = self.model.predict(val_dl)
        return pd.Series(predictions.detach().numpy().flatten())
