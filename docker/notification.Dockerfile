# get base image
FROM python:slim-buster

WORKDIR /notification

# Copy dependency file and install dependencies
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# Copy consumer script to Docker image from parent directory
COPY ../src/notification.py .

CMD [ "python", "./notification.py" ]