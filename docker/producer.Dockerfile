# get base image
FROM python:slim-buster

WORKDIR /producer

# Copy dependency file and install dependencies
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# Copy producer script to Docker image from parent directory
COPY ../src/producer.py .

CMD [ "python", "./producer.py" ]