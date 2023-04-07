FROM python:3.8-slim
WORKDIR .
COPY . /
# COPY requirements.txt .
RUN python3 -m pip install -r \
    requirements.txt --quiet
    # && rm -f requirements.txt
# ADD ./src .
ENTRYPOINT python3 src/main.py