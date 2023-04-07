import os
import pandas as pd
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import classification_report

def train_models(X_train, X_test, y_train, y_test, X, y, params):
    '''
    train, store model results: images + scores, and store models
    input:
            X_train: X training data
            X_test: X testing data
            y_train: y training data
            y_test: y testing data
    output:
            y_train_preds_rf:
            y_train_preds_lr:
            y_test_preds_lr
            y_test_preds_rf
            cv_rfc
    '''
    # This cell may take up to 15-20 minutes to run
        # train test split 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.3, random_state=42)

        # grid search
    # rfc = RandomForestClassifier(random_state=42)
        # Use a different solver if the default 'lbfgs' fails to converge
        # Reference: https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
    lrc = LogisticRegression(solver='lbfgs', max_iter=3000)

    # cv_rfc = GridSearchCV(estimator=rfc, param_grid=params, cv=5)
    # cv_rfc.fit(X_train, y_train)

    lrc.fit(X_train, y_train)

    # y_train_preds_rf = cv_rfc.best_estimator_.predict(X_train)
    # y_test_preds_rf = cv_rfc.best_estimator_.predict(X_test)

    y_train_preds_lr = lrc.predict(X_train)
    y_test_preds_lr = lrc.predict(X_test)

    # scores
    # print('random forest results')
    # print('test results')
    # print(classification_report(y_test, y_test_preds_rf))
    # print('train results')
    # print(classification_report(y_train, y_train_preds_rf))

    print('logistic regression results')
    print('test results')
    print(classification_report(y_test, y_test_preds_lr))
    print('train results')
    print(classification_report(y_train, y_train_preds_lr))
    # return y_train_preds_rf, y_train_preds_lr, y_test_preds_lr, y_test_preds_rf, cv_rfc
    return y_train_preds_lr, y_test_preds_lr, lrc