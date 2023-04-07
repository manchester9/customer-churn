import requests
import json

# Define the Seldon Core endpoint
endpoint = "http://<seldon-core-service>/seldon/<model-name>/api/v1.0/batch"

# Define the input and output file locations on GCS
input_file = "gs://<bucket>/<path>/weekly_file.csv"
output_file = "gs://<bucket>/<path>/output_file.csv"

# Define the Batch Job configuration
job_config = {
    "inputPath": input_file,
    "outputPath": output_file,
    "seldonDeploymentName": "<model-name>",
    "storageType": "gcs"
}

# Submit the Batch Job to Seldon
response = requests.post(endpoint, json=job_config)

# Monitor the progress of the Batch Job
job_id = response.json()["id"]
job_status = ""

while job_status != "completed":
    status_response = requests.get(endpoint + "/" + job_id)
    job_status = status_response.json()["status"]
    
# Access the output file on GCS
# ...


##### trigger with google cloud event #####
# Create a Cloud Function that is triggered by a GCS event
# In the Cloud Function, extract the input file path from the GCS event metadata and create a new Batch Job configuration object.
# Use the Seldon API to submit the Batch Job to your Seldon deployment, using the configuration object created in step 2.
# Monitor the progress of the Batch Job until it is completed, and handle any errors or exceptions that may occur.
# Optionally, clean up any temporary files or resources created by the Batch Job.




