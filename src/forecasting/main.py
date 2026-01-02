import pandas as pd
from forecasting.statsmodels_sarimax import StatsmodelsSARIMAX
from forecasting.sktime_ml import SKTimeML
from forecasting.darts_nbeats import DartsNBEATS
from forecasting.pytorch_tft import PyTorchTFT
from forecasting.gluonts_deepar import GluonTSDeepAR

df = pd.read_csv("stock_prices.csv", parse_dates=["Date"], index_col="Date")
series = df["Close"]

# Statsmodels
sarima = StatsmodelsSARIMAX(order=(2,1,2))
sarima.fit(series)
print("SARIMA forecast:", sarima.forecast(steps=30))

# sktime
ml_model = SKTimeML()
ml_model.fit(series)
print("ML forecast:", ml_model.forecast(steps=30))

# Darts
darts = DartsNBEATS(input_chunk=30, output_chunk=10)
darts.fit(series)
print("Darts forecast:", darts.forecast(steps=30))

# PyTorch TFT
tft = PyTorchTFT(config={"min_enc": 10, "max_enc": 30, "min_pred": 10, "max_pred": 30})
tft.fit(series)
print("TFT forecast:", tft.forecast(steps=30))

# GluonTS DeepAR
gluonts = GluonTSDeepAR(freq="D", pred_len=30)
gluonts.fit(series)
print("GluonTS forecast:", gluonts.forecast(steps=30))

# Prophet
prophet = ProphetForecaster()
prophet.fit(series)
print("Prophet forecast:", prophet.forecast(steps=30))

# Statsmodels ETS
ets = StatsmodelsETS()
ets.fit(series)
print("ETS forecast:", ets.forecast(steps=30))

# TBATS
bats = TBATSForecaster()
bats.fit(series)
print("TBATS forecast:", bats.forecast(steps=30))
