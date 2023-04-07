# import os
import pandas as pd
# import joblib
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

# from sklearn.preprocessing import normalize
# from sklearn.model_selection import train_test_split

# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import GridSearchCV

# from sklearn.metrics import classification_report

import logging
import sys

from encode import encoder_helper, perform_feature_engineering
from train import train_models

import argparse
import joblib

from google.cloud import storage

def main(run_id: str, dest_bucket_uri: str, source_file: str,):
    """
    Description:
    Args:
    Returns:
    """

    def save_model(model, model_folder, dest_bucket_uri, run_id):
        # Set up the GCS client and bucket
        client = storage.Client()

        bucket = client.get_bucket(dest_bucket_uri[5:])
        blob = bucket.blob(f'{run_id}/{model_folder}/{model}')
        blob.upload_from_filename(f'{model}')

    logging.basicConfig(stream = sys.stdout)
    logger = logging.getLogger("churn")
    logger.setLevel("INFO")

    category_list = [
        'Gender',
        'Education_Level',
        'Marital_Status',
        'Income_Category',
        'Card_Category'                
    ]

    # columns used for X
    KEEP_COLS = [
        'Customer_Age',
        'Dependent_count',
        'Months_on_book',
        'Total_Relationship_Count',
        'Months_Inactive_12_mon',
        'Contacts_Count_12_mon',
        'Credit_Limit',
        'Total_Revolving_Bal',
        'Avg_Open_To_Buy',
        'Total_Amt_Chng_Q4_Q1',
        'Total_Trans_Amt',
        'Total_Trans_Ct',
        'Total_Ct_Chng_Q4_Q1',
        'Avg_Utilization_Ratio',
        # 'Gender_Churn',
        # 'Education_Level_Churn',
        # 'Marital_Status_Churn',
        # 'Income_Category_Churn',
        # 'Card_Category_Churn'
    ]

    params = {
        'n_estimators': [200, 500],
        'max_features': ['auto', 'sqrt'],
        'max_depth': [4, 5, 100],
        'criterion': ['gini', 'entropy']
    }

    # read in data
    logger.info("Read in data")
    input_df = pd.read_csv(source_file)

    response = "Churn"
    input_df[response] = input_df['Attrition_Flag'].apply(lambda val: 0 if val == "Existing Customer" else 1)

    logger.info("Feature engineering")
    # TODO: need better code to prevent target leakage
    # encoded_df = encoder_helper(input_df, category_list, 'Churn')
    # print(encoded_df.head(5))

    # data split
    X_TRAIN, X_TEST, Y_TRAIN, Y_TEST, X, y = perform_feature_engineering(
        input_df, KEEP_COLS, response
    )

    logger.info("Train models")
    # train models with params
    # Y_TRAIN_PREDS_LR, Y_TRAIN_PREDS_RF, Y_TEST_PREDS_LR, Y_TEST_PREDS_RF, CV_RFC = train_models(
    #     X_TRAIN, X_TEST, Y_TRAIN, Y_TEST, X, y, params
    # )
    Y_TRAIN_PREDS_LR, Y_TEST_PREDS_LR, LRC = train_models(
        X_TRAIN, X_TEST, Y_TRAIN, Y_TEST, X, y, params
    )
    logger.info("Done training")

    model = "model.joblib"
    joblib.dump(LRC, model)
    save_model(model = model, model_folder = "lrc", dest_bucket_uri = dest_bucket_uri, run_id = run_id)
    
    logger.info("Saved model to GCS")
    


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Train churn models')
    parser.add_argument('--run-id', type=str, help='Pipeline run id.')
    parser.add_argument('--dest-bucket-uri', type=str, help='Destination bucket uri.')
    parser.add_argument('--source-file', type=str, help='GCS path to the train data')
    args = parser.parse_args()
    main(run_id = args.run_id, 
         dest_bucket_uri = args.dest_bucket_uri,
         source_file = args.source_file
    )
