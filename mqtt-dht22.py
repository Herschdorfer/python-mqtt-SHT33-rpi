
import os
import time
import sys
import Adafruit_DHT
import paho.mqtt.client as mqtt
import json

#sensor config
sensor = Adafruit_DHT.DHT22
pin = 22

sensor_data = {'temperature': 0, 'humidity': 0}

#openhab config
OPENHAB = 'localhost'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=10

next_reading = time.time() 

client = mqtt.Client()

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(OPENHAB, 1883, 60)

client.loop_start()

try:
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		humidity = round(humidity, 3)
		temperature = round(temperature, 3)
		sensor_data['temperature'] = temperature
		sensor_data['humidity'] = humidity

		# Sending humidity and temperature data to ThingsBoard
		client.publish('workingroom/sensors/temperature2', temperature , 1)
		client.publish('workingroom/sensors/humidity', humidity , 1)

		next_reading += INTERVAL
		sleep_time = next_reading-time.time()
		if sleep_time > 0:
			time.sleep(sleep_time)
except KeyboardInterrupt:
	pass

client.loop_stop()
client.disconnect()
