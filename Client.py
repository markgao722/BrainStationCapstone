import pandas as pd
from datetime import datetime as dt

samples = pd.DataFrame({"File": ["File 1", "File 2", "File 3", "File BADD"],
                        "Date": [dt.fromisoformat("2020-01-01"),
                                 dt.fromisoformat("2020-02-14"),
                                 dt.fromisoformat("2020-03-07"),
                                 dt.fromisoformat("2020-09-21")]})

date_labels = pd.DataFrame({"Date": [dt.fromisoformat("2020-01-01"),
                                     dt.fromisoformat("2020-02-14"),
                                     dt.fromisoformat("2020-03-07"),
                                     dt.fromisoformat("2021-01-01")],
                            "Change": ["Increase", "Increase", "Decrease", "Increase"]})

df = samples.join(date_labels.set_index('Date'), on='Date', how='inner', lsuffix="LDate", rsuffix="RDate")

print(df.head())