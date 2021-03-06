import requests
import json
import pandas as pd
import numpy as np
from datetime import timedelta


"""
Mark Gao - Capstone Project 2020.
Module 4 of 5.
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

    df.drop(['Date', 'Value', 'Pct-Chng'], axis=1, inplace=True)
        # Date (str)            not needed in model
        # Value (int)           not needed in model
        # Date-Idx (datetime)   use this to associate articles of the week to the correct weekly sample
        # Pct-Chng (float)      not needed in model
        # Change (str)          use this as class labels
    if display:
        print(df.head(10))
        print(df.tail())

    return df


def status_by_week(files: dict, EIA: pd.DataFrame)-> dict:
    """
    Once weekly oil supplies are pulled into a DataFrame (EIA), and a collection of news articles are gathered as a
        dictionary (files), use this to determine whether an article belonging to a certain date corresponded with a
        week of increased or decreased oil supply
    :param files:   dict, with keys: filename (str) and values: publication date (datetime)
    :param EIA:     pd.DataFrame, of time-series data, with column 0: date and 1: increase/decrease
    :return:        dict, with keys: publication date (datetime) and values: increase/decrease (str)
    """
    statuses = dict()

    for article_date in files.values():
        status_for_this_week = None

        for week_end, idx in zip(EIA.iloc[:, 0], range(len(EIA))):
            week_start = week_end - timedelta(days=6)

            if week_start <= article_date <= week_end:
                status_for_this_week = EIA.iloc[idx, 1]

        statuses[article_date] = status_for_this_week

    return statuses
