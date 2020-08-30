import WebScrape
import EnergyAPI
import CleanHTML
import pandas as pd
from datetime import datetime, timedelta

"""
Mark Gao - Capstone Project 2020.
Module X of X.
SUBMISSION SAMPLE. This is the order in which all functions should be run by someone seeking to
replicate the experiment for the first time on your own machine. Please remember to adjust constants
on this page as needed.
"""


# === Constants ===============================================================
root = "C:/Users/Mark/Documents/BS-CAPSTONE/BrainStationCapstone"

htmlfiles = ["raw-data",
             ]

classes = ["unlabelled"]
# =============================================================================


samples = CleanHTML.associate_dates(root, htmlfiles, classes) # contains dict{filename str: datetime obj}
EIA_df = EnergyAPI.main(display=False)
EIA_df = EIA_df.iloc[:550, :]  # don't need pre-2011 data

date_labels = EnergyAPI.status_by_week(samples, EIA_df) # constains dict{datetime obj: change str}

files = list(samples.keys())
file_dates = list(samples.values())
change_dates = list(date_labels.keys())
changes = list(date_labels.values())

df1 = pd.DataFrame({"Filename": files, "Date": file_dates}, index=range(len(files)))
df2 = pd.DataFrame({"Date": change_dates, "Change": changes}, index=range(len(changes)))
data = df2.join(df1.set_index('Date'), on='Date', how='inner', lsuffix="LDate", rsuffix="RDate")  # must join on idx

print(data.head())
