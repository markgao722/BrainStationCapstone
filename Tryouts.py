import WebScrape
import EnergyAPI
import CleanHTML
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

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

date_labels = EnergyAPI.status_by_week(samples, EIA_df) # contains dict{datetime obj: change str}

files = list(samples.keys())
file_dates = list(samples.values())
change_dates = list(date_labels.keys())
changes = list(date_labels.values())

df1 = pd.DataFrame({"Filename": files, "Date": file_dates}, index=range(len(files)))
df2 = pd.DataFrame({"Date": change_dates, "Change": changes}, index=range(len(changes)))
data = df2.join(df1.set_index('Date'), on='Date', how='inner', lsuffix="LDate", rsuffix="RDate")  # must join on idx

print(data.head())

X = data['Filename']
y = data['Change']

y_train = y.iloc[:700]
y_test = y.iloc[700:]

X_train = list()
X_test = list()

for filename in X.iloc[:700]:
    filepath = root + "/raw-data/unlabelled/" + filename

    with open(filepath, 'r', encoding='utf8') as file:
        html = file.read()
        soup = BeautifulSoup(html, features='lxml')
        tag_instances = soup.find_all('p')

        textblob = ""
        for tag in tag_instances:
            textblob += tag.text

        X_train.append(textblob)

for filename in X.iloc[700:]:
    filepath = root + "/raw-data/unlabelled/" + filename

    with open(filepath, 'r', encoding='utf8') as file:
        html = file.read()
        soup = BeautifulSoup(html, features='lxml')
        tag_instances = soup.find_all('p')

        textblob = ""
        for tag in tag_instances:
            textblob += tag.text

        X_test.append(textblob)

vectorizer = CountVectorizer(min_df=30,
                             tokenizer=None,
                             ngram_range=(1, 3))

print(len(X_train))
X_train = vectorizer.fit_transform(X_train)

print(X_train.shape)
print(y_train.shape)
logit = LogisticRegression()
logit.fit(X_train, y_train)
print(logit.score(X_train, y_train))
