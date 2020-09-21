import pandas as pd
# import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA  # KernelPCA
# from sklearn.preprocessing import StandardScaler


"""
Mark Gao - Capstone Project 2020.
Module 5 of 5.
Use this module to fit an NLP model.
"""


def prepare(X_train, X_test)-> tuple:
    """

    :param X_train:
    :param X_test:
    :return:
    """
    vectorizer = CountVectorizer(tokenizer=None,
                                 ngram_range=(1, 3),
                                 )

    X_train_mtx = vectorizer.fit_transform(X_train['Data'])
    X_test_mtx = vectorizer.transform(X_test['Data'])

    X_train_ = pd.DataFrame(data=X_train_mtx.toarray(),
                            columns=vectorizer.get_feature_names())
    X_test_ = pd.DataFrame(data=X_test_mtx.toarray(),
                           columns=vectorizer.get_feature_names())

    return X_train_, X_test_


def model_one(X_train, X_test, y_train, y_test, metrics=True)-> tuple:
    """
    Run the first experiment, which was done with a decision tree model. Use this like a class method.
    WARNING: all "model" methods take a very long time to run.
    :param X_train:
    :param X_test:
    :param y_train:
    :param y_test:
    :param metrics: bool, print out the key metrics when true.
    :return:        tuple, containing various results of the model
    """

    pipe = Pipeline([
                     ('PCA', PCA()),
                     ('Model', DecisionTreeClassifier()),
                     ])

    grid = GridSearchCV(pipe, param_grid={'PCA__n_components': list(range(1, 10)),
                                          'Model__max_depth': list(range(1, 10)),
                                          'Model__criterion': ['gini', 'entropy'],
                                          'Model__splitter': ['best', 'random'],
                                          },
                        verbose=1)

    model = grid.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    best_est = model.best_estimator_

    if metrics:
        print(f"Model 1 train score: {train_score}")
        print(f"Model 1 test score: {test_score}")
        print(f"Model 1 best estimator: {best_est}")

    return test_score, best_est


def model_two(X_train, X_test, y_train, y_test, metrics=True)-> tuple:
    """
    Run the second experiment. Use like a static method.
    >> See model_one for the parameter descriptions.
    """

    pipe = Pipeline([
                     ('PCA', PCA()),
                     ('Model', RandomForestClassifier()),
                     ])

    grid = GridSearchCV(pipe, param_grid={'PCA__n_components': list(range(1, 10)),
                                          'Model__n_estimators': [2, 5, 10, 25, 50],
                                          'Model__max_depth': list(range(1, 10)),
                                          'Model__criterion': ['gini', 'entropy'],
                                          },
                        verbose=1)

    model = grid.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    best_est = model.best_estimator_

    if metrics:
        print(f"Model 2 train score: {train_score}")
        print(f"Model 2 test score: {test_score}")
        print(f"Model 2 best estimator: {best_est}")

    return test_score, best_est


def model_three(X_train, X_test, y_train, y_test, metrics=True)-> tuple:
    """
    Run the third experiment. Use like a static method.
    >> See model_one for the parameter descriptions.
    """

    pipe = Pipeline([
        ('PCA', PCA()),
        ('Model', LogisticRegression(max_iter=300, solver='saga')),
    ])

    grid = GridSearchCV(pipe, param_grid={'PCA__n_components': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                          'Model__penalty': ['l1', 'l2', 'elasticnet'],
                                          'Model__C': [1, 10, 100, 1000]
                                          },
                        verbose=1)

    model = grid.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    best_est = model.best_estimator_

    if metrics:
        print(f"Model 3 train score: {train_score}")
        print(f"Model 3 test score: {test_score}")
        print(f"Model 3 best estimator: {best_est}")

    return test_score, best_est

def model_four(X_train, X_test, y_train, y_test, metrics=True)-> tuple:
    """
    Run the fourth experiment. Use like a static method.
    >> See model_one for the parameter descriptions.
    """

    pipe = Pipeline([
        ('PCA', PCA()),
        ('Model', LinearSVC(max_iter=1000)),
    ])

    grid = GridSearchCV(pipe, param_grid={'PCA__n_components': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                          'Model__penalty': ['l2'],
                                          'Model__loss': ['hinge', 'squared_hinge'],
                                          'Model__C': [1, 10, 100, 100]
                                          },
                        verbose=1)

    model = grid.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    best_est = model.best_estimator_

    if metrics:
        print(f"Model 4 train score: {train_score}")
        print(f"Model 4 test score: {test_score}")
        print(f"Model 4 best estimator: {best_est}")

    return test_score, best_est


def model_five(X_train, X_test, y_train, y_test, metrics=True)-> tuple:
    """
    Run the fifth experiment. Use like a static method.

    """
    vocabulary = []

    for sample in X_train:
        words = sample.split(" ")

        for n in words:
            vocabulary += n

    token = Tokenizer(oov_token="<OOV>")
    token.fit_on_texts(vocabulary)


    model = keras.Sequential([
        keras.layers.Embedding(10000, 16, input_length=120),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid'),
        ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return (model.summary())
