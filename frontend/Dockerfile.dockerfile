FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

# Download the model from GCS and put it in container
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://storage.googleapis.com/[YOUR-BUCKET-NAME]/[PATH-TO-MODEL]/model.pkl -O /app/model.pkl && \
    apt-get remove -y wget && \
    rm -rf /var/lib/apt/lists/*

# Copy the service account key
COPY service_account_key.json .

ENV GOOGLE_APPLICATION_CREDENTIALS /app/service_account_key.json

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

