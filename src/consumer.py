"""
This script is responsible for consuming the data from the MQTT broker
"""

import json
import logging
import sqlite3
import requests
import paho.mqtt.client as mqtt

MQTT_BROKER_IP = "broker.hivemq.com"  # Replace with your MQTT broker IP
MQTT_PORT = 1883
TOPIC = "unisinos/feilke/weather_station/data"
DATABASE_FILE = "weather_station.db"  # SQLite Database file


def on_connect(client_instance, __userdata__, __flags__, rc, __properties__):
    """Handle the on_connect event from the MQTT broker

    Args:
        client (_type_): The client instance for this callback
        __userdata__ (_type_): _description_
        __flags__ (_type_): _description_
        rc (_type_): Result code from the connection
        __properties__ (_type_): _description_
    """
    print("Connected with result code " + str(rc))
    client_instance.subscribe(TOPIC)


def on_message(client, userdata, msg):
    """Handle the on_message event from the MQTT broker

    Args:
        client (mqtt.Client): The client instance for this callback
        userdata (obj): The private user data as set in Client() or userdata_set()
        msg (mqtt.MQTTMessage): An instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
    """

    # Decode the MQTT message payload and load it as a JSON object
    message_json = msg.payload.decode("utf-8")
    cloud_event = json.loads(message_json)

    # Extract data from the CloudEvent
    data = cloud_event["data"]

    check_temperature_and_notify(data, 30, "http://127.0.0.1:5000/")

    client_id = data["client_id"]
    user_id = data["userId"]
    temperature = data["temperature"]
    timestamp = data["timestamp"]
    correlation_id = data["correlation_id"]
    logging.info(
        f"Analyzing data. Client ID: {client_id}, User ID: {user_id}, T: {temperature}, Timestamp: {timestamp}, Correlation ID: {correlation_id}"
    )

    # Save to SQLite database
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS WeatherData 
        (client_id text, user_id text, temperature real, timestamp text, correlation_id text)
        """
    )
    insert_query = """
    INSERT INTO WeatherData 
    (client_id, user_id, temperature, timestamp, correlation_id) 
    VALUES (?, ?, ?, ?, ?)"""

    c.execute(
        insert_query, (client_id, user_id, temperature, timestamp, correlation_id)
    )
    conn.commit()
    conn.close()


def check_temperature_and_notify(data, threshold, url):
    """Check if the temperature surpasses the threshold and notify an HTTP endpoint if it does.

    Args:
        data (dict): The data dictionary containing temperature and other fields.
        threshold (float): The temperature threshold.
        url (str): The URL of the HTTP endpoint to notify.
    """
    if data["temperature"] > threshold:
        # The temperature surpasses the threshold, prepare the payload
        payload = {
            "client_id": data["client_id"],
            "user_id": data["userId"],
            "event_type": "temperature.overheat",
            "timestamp": data["timestamp"],
            "severity": 7,  # replace with actual severity if available in data
            "correlation_id": data["correlation_id"],
        }

        # Make an HTTP request to the endpoint
        try:
            response = requests.post(url, json=payload)
            # Check if the request was successful
            if response.status_code == 200:
                logging.info(
                    f"Notification sent successfully. Temperature: {data['temperature']}"
                )
            else:
                logging.warn(
                    f"Failed to send notification. Status code: {response.status_code}"
                )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send notification. Error: {str(e)}")
            return


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "WeatherStationConsumer")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_IP, port=MQTT_PORT)

client.loop_forever()
