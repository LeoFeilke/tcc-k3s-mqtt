import paho.mqtt.client as mqtt
import time
import random
import json

mqtt_broker_ip = "broker.hivemq.com"  # Replace with your MQTT broker IP
mqtt_port = 1883
topic = "unisinos/feilke/weather_station/data"

def on_connect(__client__, __userdata__, __flags__, rc, __properties__):
    if rc == 0:
        print("Connected to MQTT broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

# Create new instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "WeatherStationProducer")

client.on_connect = on_connect

# Connecting to broker
client.connect(mqtt_broker_ip, port=mqtt_port)

client.loop_start()

try:
    while True:
        temperature = round(random.uniform(18.0, 28.0), 2)
        humidity = round(random.uniform(40, 60), 2)
        wind_speed = round(random.uniform(2, 10), 2)
        message = {"temperature": temperature, "humidity": humidity, "wind_speed": wind_speed}
        message_json = json.dumps(message)
        client.publish(topic, message_json)
        print(f"Published message {message} to topic {topic}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting")
    client.loop_stop()
    client.disconnect()
