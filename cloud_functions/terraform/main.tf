resource "google_cloudfunctions2_function" "trigger_train_pipeline" {
  project     = var.project_id
  name        = "trigger-train-pipeline"
  location    = "europe-west1"
  description = "Event Driven Cloud Function, load "

  build_config {
    runtime     = "python310"
    entry_point = "save_gcs_file_to_bq_function"
    source {
      storage_source {
        bucket = "mazlum_dev"
        object = "cloud_functions/functions/saving_job_failures_bq/saving_job_failures_bq.zip"
      }
    }
  }

  service_config {
    max_instance_count             = 3
    min_instance_count             = 1
    available_memory               = "1Gi"
    timeout_seconds                = 120
    ingress_settings               = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
    service_account_email          = "sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com"
  }

  event_trigger {
    trigger_region        = "europe-west1"
    event_type            = "google.cloud.storage.object.v1.finalized"
    service_account_email = "sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com"
    event_filters {
      attribute = "bucket"
      value     = "event-arc-trigger-function"
    }
  }
}