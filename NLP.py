import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import fetch_20newsgroups


"""
Mark Gao - Capstone Project 2020.
Module 3 of X.
Use this module to fit an NLP model.
"""


categorical = ['alt.atheism', 'comp.graphics', 'sci.med', 'soc.religion.christian']
bunch = fetch_20newsgroups(subset='train', categories=categorical, shuffle=True, random_state=42)
bunch_ = fetch_20newsgroups(subset='test', categories=categorical, shuffle=True, random_state=42)
    # bunch:       sklearn.utils.Bunch object
    # bunch.data:  list object
    # bunch.target:    np.array object
    # bunch.target_names:  list object (unique classes)

data = bunch.data
# ["This article is about...",
#  "New York News: Today on Wall Street over a thousand...",
#  "Apple announces $2.0 billion in funding..."]

labels = bunch.target
# np.array([0, 1, 3, 3, 2, ...])

labelnames= bunch.target_names
# Equivalent to categorical = ['alt.atheism', 'comp.graphics', 'sci.med', 'soc.religion.christian']

vectorizer = CountVectorizer(min_df=15,
                             tokenizer=None,
                             ngram_range=(1, 2))  # CountVectorizer object

X_train = vectorizer.fit_transform(data)  # scipy sparse csr_matrix

# Using the vectorizer as one-hot encoded columns and the matrix as word counts and samples, we can visualize the data
#   in a DataFrame.
df = pd.DataFrame(columns=vectorizer.get_feature_names(),
                  data=X_train.toarray())

print(df.head())
print(df.shape)

logit = LogisticRegression()
logit.fit(X_train, labels)
print(logit.score(X_train, labels))

# Test data portion of things ----------
data_ = bunch_.data
X_test = vectorizer.transform(data_)
labels_ = bunch_.target

df = pd.DataFrame(columns=vectorizer.get_feature_names(),
                  data=X_test.toarray())

print(df.head())
print(df.shape)
# --------------------------------------

preds = logit.predict(X_test)
print(accuracy_score(preds, labels_))
