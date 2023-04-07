from google.cloud import aiplatform
# import pandas as pd

import argparse


# example way to run file
# python3 vertex_ai_deploy.py \
# --project_id "united-impact-363519" \
# --region "us-central1" \
# --model_display_name "Churn Model" \
# --model_description "Churn Classification Mode" \
# --model_artifact_uri "gs://churn_data_363519/churn-prediction-pipeline-20230406190623/lrc" \
# --model_serving_container_image_url "us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest" \
# --endpoint_id "3280815153934761984" \
# --machine_type "n1-standard-2"


def deploy_model(project_id, 
                 region, 
                 model_display_name, 
                 model_description, 
                 model_artifact_uri, 
                 model_serving_container_image_url, 
                 endpoint_id,
                 machine_type
    ):

    print("Initialize AI Platform")
    aiplatform.init(project=project_id, location=region)

    print("Upload model")
    # Importing model artifacts
    model = aiplatform.Model.upload(
        display_name = model_display_name,
        description = model_description,
        artifact_uri = model_artifact_uri,
        serving_container_image_uri = model_serving_container_image_url
    )

    if len(endpoint_id) == 0:
        print("Create endpoint")
        # create endpoint if not specified
        endpoint = aiplatform.Endpoint.create(display_name = 'Churn Model Endpoint', 
                                            project = project_id, 
                                            location = region)
        endpoint_id = endpoint.name
    else:
        print("Use existing endpoint")
        endpoint = aiplatform.Endpoint(endpoint_name = endpoint_id)

    
    print("Deploy model to endpoint ")
    model.deploy(endpoint = endpoint,
            machine_type = machine_type
    )

    print("Done")

    # To undeploy model:
    # You pay for each model deployed to an endpoint, even if no prediction is made. 
    # You must undeploy your model to stop incurring further charges. 
    # Models that are not deployed or have failed to deploy are not charged.
    # endpoint.undeploy(deployed_model_id="5501571356321382400")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Deploy churn model')
    parser.add_argument('--project_id', type=str, help='Project ID.')
    parser.add_argument('--region', type=str, help='region location')
    parser.add_argument('--model_display_name', type=str, help='model display name')
    parser.add_argument('--model_description', type=str, help='model description')
    parser.add_argument('--model_artifact_uri', type=str, help='where model is saved on GCS')
    parser.add_argument('--model_serving_container_image_url', type=str, help='image model is served in')
    parser.add_argument('--endpoint_id', type=str, help='Endpoint ID')
    parser.add_argument('--machine_type', type=str, help='machine type for model deployment')

    args = parser.parse_args()

    deploy_model(
        project_id = args.project_id, 
        region = args.region,
        model_display_name=args.model_display_name,
        model_description = args.model_description,
        model_artifact_uri = args.model_artifact_uri,
        model_serving_container_image_url = args.model_serving_container_image_url,
        endpoint_id = args.endpoint_id,
        machine_type = args.machine_type
    )

