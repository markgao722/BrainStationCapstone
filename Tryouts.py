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
energy_df = EnergyAPI.main(display=False)
mapper_df = energy_df[['Date-Idx', 'Change']]
mapper_df = mapper_df.iloc[:550, :]

status_by_week = dict()

for article_date in samples.values():
    status_for_this_week = None

    for week_end, idx in zip(mapper_df["Date-Idx"], range(len(mapper_df))):
        week_start = week_end - timedelta(days=6)

        if week_start <= article_date <= week_end:
            status_for_this_week = mapper_df.iloc[idx, 1]

    status_by_week[article_date] = status_for_this_week
    print(status_for_this_week)

print(status_by_week)
