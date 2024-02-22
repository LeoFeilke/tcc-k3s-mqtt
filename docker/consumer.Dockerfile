# get base image
FROM python:slim-buster

WORKDIR /consumer

# Copy dependency file and install dependencies
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# Copy consumer script to Docker image from parent directory
COPY ../src/consumer.py .

CMD [ "python", "./consumer.py" ]