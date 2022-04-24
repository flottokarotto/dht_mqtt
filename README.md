# Description
Read temperature/humidity from DHT Sensor using pigpio and send the results to a mqtt broker.
Intended to use with Home Assistant and Raspberry Pi.

The Broker url and the topics are hard coded. 

# Installation
- pip install pigpio-dht
- pip install paho-mqtt
- sudo apt install pigpio

# Usage 
Modify the GPIO number, MQTT URL and MQTT topic to your need and run it with cron or systemd timer.


