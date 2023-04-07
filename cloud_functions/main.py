import functions_framework
from google.cloud import aiplatform

PROJECT_ID = 'designing-ml-systems-382919'         # <---CHANGE THIS
REGION = 'us-central1'                 # <---CHANGE THIS
# this is where pipeline output information is saved off ()
PIPELINE_ROOT = 'gs://vertex_pipeline_hello_world_01/logs'   # <---CHANGE THIS
DISPLAY_NAME = 'churn_pipeline'

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")
    
    aiplatform.init(
       project=PROJECT_ID,
       location=REGION,
    )

    # the training data location
    # this is the new file uploaded to the training data bucket
    SOURCE_FILE = "gs://" + bucket + "/" + name

    # parameters to pass into pipeline
    parameter_values = {
        "dest_bucket_uri": "gs://churn_data_382919",
        "source_file": SOURCE_FILE
    }

    # The output of compiling the pipeline
    pipeline_spec_uri = "gs://churn_data_382919/churn_pipeline.json"

    job = aiplatform.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path=pipeline_spec_uri,
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
        parameter_values=parameter_values
    )

    job.submit()
    return "Job submitted"
