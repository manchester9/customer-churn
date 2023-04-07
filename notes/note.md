driver_script.py

churn_library.py

Steps:
- Ingest Data
- EDA
- Encoding DF
- Split data
- Training
- Output results
- Save model to GCS bucket
- cloud function gets triggered when new model object is saved
- cloud function dockerizes environment and pushes to kubernetes
- vertex AI deployment or using seldon to delploy on kubernetes
