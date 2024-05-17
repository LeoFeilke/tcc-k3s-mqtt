"""
This script is responsible for consuming the data from the MQTT broker
"""

import json
import sqlite3
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


def on_message(__client__, __userdata__, msg):
    """Handle the on_message event from the MQTT broker

    Args:
        __client__ (_type_): _description_
        __userdata__ (_type_): _description_
        msg (_type_): The message received from the MQTT broker
    """

    message_json = msg.payload.decode("utf-8")
    message = json.loads(message_json)
    temperature = message["temperature"]
    humidity = message["humidity"]
    wind_speed = message["wind_speed"]
    print(f"Analyzing data. T: {temperature}, H: {humidity}, WS: {wind_speed}")

    # Save to SQLite database

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS WeatherData 
        (temperature real, humidity real, wind_speed real)
        """
    )
    insert_query = f"""
    INSERT INTO WeatherData 
    (temperature, humidity, wind_speed) 
    VALUES ({temperature}, {humidity}, {wind_speed})"""

    c.execute(insert_query)
    conn.commit()
    conn.close()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "WeatherStationConsumer")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_IP, port=MQTT_PORT)

client.loop_forever()
