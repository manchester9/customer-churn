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

def encoder_helper(df, category_lst, response):
    '''
    TODO: to prevent leakage, we need to use smarter code (does not make sense to calculate these columns for the test set)
    helper function to turn each categorical column into a new column with
    proportion of churn for each category - associated with cell 15 from the notebook
    input:
            df: pandas dataframe
            category_lst: list of columns that contain categorical features
            response: string of response name [optional argument that could be used for naming variables or index y column]
    output:
            df: pandas dataframe with new columns for
    '''
    df[response] = df['Attrition_Flag'].apply(lambda val: 0 if val == "Existing Customer" else 1)
    for cat in category_lst:
        df[cat + '_' + response] = df[cat].map(df.groupby(cat).mean()[response])
    return df

def perform_feature_engineering(df, cols, response):
    '''
    input:
            df: pandas dataframe
            cols: string of response name [optional argument that could be used for naming variables or index y column]
    output:
            X_train: X training data
            X_test: X testing data
            y_train: y training data
            y_test: y testing data
    '''
    y = df[response]
    X = pd.DataFrame()
    X[cols] = df[cols]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

    return X_train, X_test, y_train, y_test, X, y