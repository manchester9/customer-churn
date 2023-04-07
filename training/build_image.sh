#!/bin/bash
IMAGE_TAG=$1
PROJECT_ID=$2

echo "Building image!"
docker buildx build --platform linux/amd64 -t "gcr.io/$PROJECT_ID/sample/churn_classifier:$IMAGE_TAG" .

echo "Pushing image to GCR"
docker push "gcr.io/$PROJECT_ID/sample/churn_classifier:$IMAGE_TAG"

# for testing locally
# docker run --platform linux/amd64 --name train_container -it gcr.io/united-impact-363519/sample/churn_classifier:v1.0.0 /bin/sh