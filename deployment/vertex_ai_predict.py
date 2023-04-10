from google.cloud import aiplatform
import pandas as pd
import argparse

# example way to run file
# python3 vertex_ai_predict.py \
# --project_id "united-impact-363519" \
# --region "us-central1" \
# --endpoint_id "3280815153934761984" \
# --pred_df_path "predict_data/sample_customers.csv"

def predict(project_id, region, endpoint_id, pred_df_path):

    aiplatform.init(project=project_id, location=region)

    print("Read in pred df")
    # NOTE: assumes pred_df is in the right format
    pred_df = pd.read_csv(pred_df_path)

    endpoint = aiplatform.Endpoint(endpoint_name = endpoint_id)

    print("Get predictions")
    predictions = endpoint.predict(instances=pred_df.values.tolist())

    pred_df["pred"] = predictions.predictions

    print("Write predictions")
    output_pred_path = pred_df_path.split(".")[0] + "_w_pred." + pred_df_path.split(".")[-1]
    pred_df.to_csv(output_pred_path, index=False)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Deploy churn model')
    parser.add_argument('--project_id', type=str, help='Project ID.')
    parser.add_argument('--region', type=str, help='region location')
    parser.add_argument('--endpoint_id', type=str, help='endpoint id')
    parser.add_argument('--pred_df_path', type=str, help='path to df for which we need predictions')

    args = parser.parse_args()

    predict(
        project_id = args.project_id, 
        region = args.region,
        endpoint_id = args.endpoint_id,
        pred_df_path = args.pred_df_path
    )

