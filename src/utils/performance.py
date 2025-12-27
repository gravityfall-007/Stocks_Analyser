import pandas as pd

def normalize_prices(price_df, base_col="Close"):
    """
    Normalize price series to 100 at start date.
    """
    base_value = price_df[base_col].iloc[0]
    return (price_df[base_col] / base_value) * 100
