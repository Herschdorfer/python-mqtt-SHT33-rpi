
import os
import time
import sys
import Adafruit_BMP.BMP085 as BMP085
import paho.mqtt.client as mqtt
import json

sensor = BMP085.BMP085()

OPENHAB = 'localhost'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'temperature': 0, 'pressure': 0}

next_reading = time.time() 

client = mqtt.Client()

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(OPENHAB, 1883, 60)

client.loop_start()

try:
	while True:
		temperature = sensor.read_temperature()
		pressure = sensor..read_pressure()
		pressure = round(pressure, 2)
		temperature = round(temperature, 2)
		print(u"Temperature: {:g}\u00b0C, Humidity: {:g}%".format(temperature, pressure))
		sensor_data['temperature'] = temperature
		sensor_data['humidity'] = pressure

		# Sending humidity and temperature data to ThingsBoard
		client.publish('workingroom/sensors/temperature', temperature , 1)
		client.publish('workingroom/sensors/pressure', pressure , 1)

		next_reading += INTERVAL
		sleep_time = next_reading-time.time()
		if sleep_time > 0:
			time.sleep(sleep_time)
except KeyboardInterrupt:
	pass

client.loop_stop()
client.disconnect()
