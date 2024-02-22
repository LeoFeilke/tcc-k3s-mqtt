# MQTT Producer-Consumer Application 

This project provides a simple simulation of a producer (a weather station) sending data to multiple consumers using MQTT protocol. The communication is based on the Publish/Subscribe feature of MQTT. 

The producer generates weather data every second, including temperature, humidity, and wind speed. 

## Getting Started 

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Python 3.x and pip should be installed on your system. Please also install Docker to containerize the application.

### Installing

Follow these steps to run this project in your local machine:

1. Clone the project:
```bash
git clone <project-github-url>


# Go inside the project directory:
cd <project-directory> 

## Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate  
# On Windows use `venv\Scripts\activate`

Now intall the python dependencies:

pip install -r requirements.txt
``````
### Docker
You can easily dockerize the application. Go to your project directory and build your Docker image:

#### For Producer:
```bash
docker build -t mqtt-producer -f docker/producer.Dockerfile .
``````
#### For Consumer:
```bash
docker build -t mqtt-consumer -f docker/consumer.Dockerfile .
``````

### Running
To run the Producer, navigate to the project directory and use either:

Docker:
```bash
docker run -d mqtt-producer
``````
Python:
```bash
python src/producer.py
``````

Similarly for Consumer, use either:

Docker:

```bash
docker run -d mqtt-consumer
```

Python:
```bash
python src/consumer.py
``````