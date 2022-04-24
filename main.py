#!/usr/bin/env python3
import sys
import json
import paho.mqtt.client as paho
from pigpio_dht import DHT22


client = paho.Client()
s = DHT22(4)
result = s.read()
# client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
client.connect("homeassistant", 1883, 60)

config_message_temperature = {
    "device_class": "temperature",
    "name": "Attic_Temperature",
    "state_topic": "homeassistant/sensor/attic/state",
    "unit_of_measurement": "°C",
    "value_template":
        "{{ value_json.temperature}}"
}

config_message_humidity = {
    "device_class": "humidity",
    "name": "Attic_Humidity",
    "state_topic": "homeassistant/sensor/attic/state",
    "unit_of_measurement": "%",
    "value_template":
        "{{ value_json.humidity}}"
}

client.publish("homeassistant/sensor/atticT/config",
               json.dumps(config_message_temperature), retain=True)
client.publish("homeassistant/sensor/atticH/config",
               json.dumps(config_message_humidity), retain=True)

try:

    if result["valid"]:
        temperature = result["temp_c"]
        humidity = result["humidity"]
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        client.publish("homeassistant/sensor/attic/state",
                       json.dumps({"temperature": temperature, "humidity": humidity}))
        sys.exit(0)
    else:
        print("Failed to retrieve data from sensor")
        print("Data invalid")
        sys.exit(-1)
except Exception as error:
    print("Failed to retrieve data from sensor")
    print(error.args[0])
    sys.exit(-1)
