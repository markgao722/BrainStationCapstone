import WebScrape
import EnergyAPI
import CleanHTML
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

htmlfiles = ["data-FT",
             "data-Twitter",
             ]

classes = ["bull", "bear", "neutral"]
# =============================================================================


samples = CleanHTML.associate_dates(root, htmlfiles, classes) # contains dict{filename str: datetime object}
EIA_df = EnergyAPI.main(display=False)
EIA_df = EIA_df.iloc[:550, :]

date_labels = EnergyAPI.status_by_week(samples, EIA_df)
print(date_labels)