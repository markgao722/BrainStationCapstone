import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA, KernelPCA

"""
Mark Gao - Capstone Project 2020.
Module X of X.
Use this module to fit an NLP model.
"""


def prepare(X_train, X_test)-> tuple:

    vectorizer = CountVectorizer(min_df=30,
                                 tokenizer=None,
                                 ngram_range=(1, 3),
                                 )

    X_train_ = vectorizer.fit_transform(X_train)
    X_test_ = vectorizer.transform(X_test)

    return (X_train_, X_test_)


def model_one(X_train, X_test, y_train, y_test, metrics=True)-> tuple:
    """
    Run the first trial, which was done with a decision tree model. Estimated run-time is XXX minutes.
    :param X_train: df, or Series, where the column contains strings representing articles.
    :param X_test:  df, or Series, where the column contains strings representing articles.
    :param y_train: df, or Series, where the column contains the 'increase' / 'decrease' string.
    :param y_test:  df, or Series, where the column contains the 'increase' / 'decrease' string.
    :param metrics: bool, print out the key metrics when true.
    :return:        tuple, containing various results of the model
    """

    pipe = Pipeline([('PCA', PCA()),
                     ('Model', DecisionTreeClassifier()),
                     ])

    grid = GridSearchCV(pipe, param_grid={'PCA__n_components': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                          'Model__max_depth': range(25),
                                          })

    model = grid.fit(X_train, y_train)

    test_score = model.score(X_test, y_test)
    best_est = model.best_estimator_

    if metrics:
        print(test_score)
        print(best_est)

    return (test_score, best_est)


def model_two(X_train, X_test, y_train, y_test, metrics=True)-> tuple:
    """
    Run the first trial, which was done with a random forest model. Estimated run-time is XXX minutes.
    >> See model_one for the parameter descriptions.
    :return:
    """

    pipe = Pipeline([('PCA', PCA()),
                     ('Model', RandomForestClassifier()),
                     ])

    grid = GridSearchCV(pipe, param_grid={'PCA__n_components': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                          'Model__n_estimators': [1, 2, 3, 4, 5],
                                          'Model__max_depth': range(25)})

    model = grid.fit(X_train, y_train)

    test_score = model.score(X_test, y_test)
    best_est = model.best_estimator_

    if metrics:
        print(test_score)
        print(best_est)

    return (test_score, best_est)