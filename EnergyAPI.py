import requests
import json
import pandas as pd
import numpy as np


"""
Mark Gao - Capstone Project 2020.
Module X of X.
This makes an API call to the EIA's database to collect oil stock data. An alternative is to download a CSV to local
machine. The oil supply figures (or rather the change in supplies) will be used as class labels for the model.
"""

def main(display=True)-> pd.DataFrame:
    """
    Pulls the weekly oil supply figures from the Energy Institute (US) via API call.
    :param display: bool, Print some head/tail and other helpful descriptions of the df you pulled.
    :return:        pd.DataFrame, time-series-like oil supply data
    """
    key = "353d83b81ead60c4adf18aeddf48d5b4"
    url = f"http://api.eia.gov/series/?api_key={key}&series_id=PET.WCESTUS1.W"

    response = requests.get(url)

    json_data = json.loads(response.text)
    data_ = json_data["series"]
    data_ = data_[-1]
    data = data_["data"]

    # metadata
    series = data_["description"]
    updated = data_["updated"]

    df = pd.DataFrame(data, columns=["Date", "Value"])  # value is in units of 000s barrels
    df["Date-Idx"] = pd.to_datetime(df["Date"])
    df["Pct-Chng"] = df["Value"].pct_change(-1)
    df["Change"] = np.where(df["Pct-Chng"] <= 0, "Decrease", "Increase")

    if display:
        print(df.head(10))
        print(df.tail())
        print(df.info())
        print(df.describe())

        # Date (str)            not needed in model
        # Value (int)           not needed in model
        # Date-Idx (datetime)   use this to associate articles of the week to the correct weekly sample
        # Pct-Chng (float)      not needed in model
        # Change (str)          use this as class labels
    return df
