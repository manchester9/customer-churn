from google.cloud import aiplatform as aip

from kfp.v2 import dsl
from kfp.v2 import compiler
from kfp.v2.dsl import component

from kfp.v2 import compiler  # noqa: F811
from google_cloud_pipeline_components.v1.endpoint import (EndpointCreateOp,
                                                              ModelDeployOp)
from google_cloud_pipeline_components.v1.model import ModelUploadOp

from pipeline_components import (
    perform_eda,
    train,
)

import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
DEST_BUCKET_URI = os.getenv("DEST_BUCKET_URI")
SOURCE_FILE = os.getenv("SOURCE_FILE")
PIPELINE_BUCKET_URI = os.getenv("PIPELINE_BUCKET_URI")
SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT")

# API service endpoint
API_ENDPOINT = "{}-aiplatform.googleapis.com".format(REGION)
PIPELINE_ROOT = "{}/pipeline_root/intro".format(PIPELINE_BUCKET_URI)
# print(f"PIPELINE_ROOT DEBUG: {PIPELINE_ROOT}")

@dsl.pipeline(
    name="churn-prediction-pipeline",
    description="Getting churn predictions",
    pipeline_root=PIPELINE_ROOT,
)
def pipeline(dest_bucket_uri: str, source_file: str):

    # TODO: get just the run id number from this string
    run_id = dsl.PIPELINE_JOB_NAME_PLACEHOLDER.split("-")[-1]
    
    # input_data_task = (
    #     ingest_data(source_bucket_uri = source_bucket_uri).
    #     set_cpu_limit('1').
    #     set_memory_limit('3G').
    #     set_display_name("Ingest Data")
    # )

    perform_eda_task = (
        perform_eda(run_id = run_id, 
                    dest_bucket_uri = dest_bucket_uri,
                    source_file = source_file).\
            set_cpu_limit('1').\
            set_memory_limit('3G').\
            set_display_name("Ingest Data & Perform EDA")#.\
    )
    
    train_task = train(run_id = run_id, 
          dest_bucket_uri = dest_bucket_uri, 
          source_file = source_file).\
        set_display_name("Train Models").\
        after(perform_eda_task)
    
    model_upload_op = ModelUploadOp(
        project=PROJECT_ID,
        display_name='model_upload',
        unmanaged_container_model=dest_bucket_uri,
    )
    model_upload_op.after(train_task)

    endpoint_create_op = EndpointCreateOp(
        project=PROJECT_ID,
        display_name="pipelines-created-endpoint",
    ).after(model_upload_op)

    ModelDeployOp(
        endpoint=endpoint_create_op.outputs["endpoint"],
        model=model_upload_op.outputs["model"],
        deployed_model_display_name='model_deploy',
        dedicated_resources_machine_type="n1-standard-16",
        dedicated_resources_min_replica_count=1,
        dedicated_resources_max_replica_count=1,
    ).after(endpoint_create_op)


if __name__=="__main__":


    aip.init(project=PROJECT_ID, staging_bucket=PIPELINE_BUCKET_URI)

    compiler.Compiler().compile(pipeline_func=pipeline, package_path="churn_pipeline.json")

    DISPLAY_NAME = "churn_pipeline"

    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="churn_pipeline.json",
        # pipeline_root is where information is saved off for every run
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
        parameter_values = {
            "dest_bucket_uri": DEST_BUCKET_URI,
            "source_file": SOURCE_FILE
        }
    )

    print(type(job))

    job.run()

    # clean up
    # training triger input 
    # deploy - scheduled (?) trigger POSTMAN