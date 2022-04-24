import paho.mqtt.client as paho
import json

from time import sleep
from pigpio_dht import DHT22

if __name__ == '__main__':

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

    client.publish("homeassistant/sensor/atticT/config", json.dumps(config_message_temperature), retain=True)
    client.publish("homeassistant/sensor/atticH/config", json.dumps(config_message_humidity), retain=True)

    while True:
        try:
            status = result[2]
            print(status)
            temperature = result[3]
            humidity = result[4]
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
            client.publish("homeassistant/sensor/attic/state", json.dumps({"temperature": temperature, "humidity": humidity}))
        except Exception as error:
            print("Failed to retrieve data from sensor")
            print(error.args[0])
        sleep(1)



