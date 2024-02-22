import paho.mqtt.client as mqtt
import json
import sqlite3

mqtt_broker_ip = "broker.hivemq.com"  # Replace with your MQTT broker IP
mqtt_port = 1883
topic = "unisinos/feilke/weather_station/data"
database_file = "weather_station.db"  # SQLite Database file

def on_connect(client, __userdata__, __flags__, rc, __properties__):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(__client__, __userdata__, msg):
    message_json = msg.payload.decode('utf-8')
    message = json.loads(message_json)
    temperature = message['temperature']
    humidity = message['humidity']
    wind_speed = message['wind_speed']
    print(f"Analyzing weather data. Temperature: {temperature}, Humidity: {humidity}, Wind Speed: {wind_speed}")

    # Save to SQLite database
   
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS WeatherData (temperature real, humidity real, wind_speed real)')
    insert_query = f"INSERT INTO WeatherData (temperature, humidity, wind_speed) VALUES ({temperature}, {humidity}, {wind_speed})"
    c.execute(insert_query)
    conn.commit()
    conn.close()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "WeatherStationConsumer")
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, port=mqtt_port)

client.loop_forever()