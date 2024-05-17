"""
This script is responsible for producing the data to the MQTT broker
"""

import random
import json
import time
import paho.mqtt.client as mqtt

MQTT_BROKER_IP = "broker.hivemq.com"  # Replace with your MQTT broker IP
MQTT_PORT = 1883
TOPIC = "unisinos/feilke/weather_station/data"


def on_connect(__client__, __userdata__, __flags__, rc, __properties__):
    """Handles the on_connect event from the MQTT broker

    Args:
        __client__ (_type_): _description_
        __userdata__ (_type_): _description_
        __flags__ (_type_): _description_
        rc (_type_): The result code from the connection
        __properties__ (_type_): _description_
    """
    if rc == 0:
        print("Connected to MQTT broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


# Create new instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "WeatherStationProducer")

client.on_connect = on_connect

# Connecting to broker
client.connect(MQTT_BROKER_IP, port=MQTT_PORT)

client.loop_start()

try:
    while True:
        temperature = round(random.uniform(18.0, 28.0), 2)
        humidity = round(random.uniform(40, 60), 2)
        wind_speed = round(random.uniform(2, 10), 2)
        message = {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
        }
        message_json = json.dumps(message)
        client.publish(TOPIC, message_json)
        print(f"Published message {message} to topic {TOPIC}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting")
    client.loop_stop()
    client.disconnect()
