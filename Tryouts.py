# import WebScrape
import EnergyAPI
import CleanHTML
import NLP
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split


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


# --- Step 2: Tag each article with a date and its corresponding oil event on that date. ---
samples = CleanHTML.associate_dates(root, htmlfiles, classes)  # contains dict{filename str: datetime obj}
EIA_df = EnergyAPI.main(display=False)
EIA_df = EIA_df.iloc[:550, :]  # don't need pre-2011 data

date_labels = EnergyAPI.status_by_week(samples, EIA_df)  # contains dict{datetime obj: change str}

files = list(samples.keys())
file_dates = list(samples.values())
change_dates = list(date_labels.keys())
changes = list(date_labels.values())

df1 = pd.DataFrame({"Filename": files, "Date": file_dates}, index=range(len(files)))
df2 = pd.DataFrame({"Date": change_dates, "Change": changes}, index=range(len(changes)))

# -- Result:
data = df2.join(df1.set_index('Date'), on='Date', how='inner', lsuffix="LDate", rsuffix="RDate")  # must join on idx


# --- Step 3: Using the DataFrame of article files, open each file and extract the text into a DataFrame.
#             Each entry of the DataFrame is a giant block of text representing one article.
X = data['Filename']
y = data['Change']

text_list = list()

for filename in X.iloc[:]:
    filepath = root + "/raw-data/unlabelled/" + filename

    with open(filepath, 'r', encoding='utf8') as file:
        html = file.read()
        soup = BeautifulSoup(html, features='lxml')
        tag_instances = soup.find_all('p')

        textblob = ""
        for tag in tag_instances:
            textblob += tag.text

        text_list.append(textblob)

# --- Result:
X_df = pd.DataFrame({"Data": text_list}, index=range(len(text_list)))
# Note, the beginning of every article starts with "Click here for 150+..." but the articles re actually different.


# --- Step 4: Split the data into train and test sets and begin running models.
X_train_df, X_test_df, y_train, y_test = train_test_split(X_df, y, test_size=0.33, random_state=0)
# train: 236/722 decrease, 487/722 increase
# test: 119/357 decrease, 238/357 increase

X_train, X_test = NLP.prepare(X_train_df, X_test_df)


#NLP.model_one(X_train, X_test, y_train, y_test)
#NLP.model_two(X_train, X_test, y_train, y_test)
#NLP.model_three(X_train, X_test, y_train, y_test)
#NLP.model_four(X_train, X_test, y_train, y_test)
NLP.model_five(X_train, X_test, y_train, y_test)