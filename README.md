# ML Workflow for predicting churn

## Description
The business problem in this project is predicting customer churn.

We have a cloud function that kicks off a training pipeline whenever new training data is uploaded to a specific GCP bucket.
This training pipeline is built with Vertex AI and Kubeflow and saves off eda plots and trained models to GCS.

We then use Vertex AI to deploy specific models to endpoints and serve online predictions.

## Architecture

## TODO's
- deploy cloud function with Terraform
- incorporate split training and full training modes
- add more models
- look into other deployment strategies beyond Vertex AI

## To Replicate
look at instructions.md for more details