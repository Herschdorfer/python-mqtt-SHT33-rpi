#insatll pip3 install Adafruit-SHT31 paho-mqtt Adafruit-GPI as root

from Adafruit_SHT31 import *

import os
import time
import sys
import paho.mqtt.client as mqtt
import json

sensor = SHT31(address = 0x44)

OPENHAB = 'openhabianpi'

INTERVAL=30

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time() 

client = mqtt.Client()

client.connect(OPENHAB, 1883, 60)

client.loop_start()

try:
	while True:
		temperature = sensor.read_temperature()
		humidity = sensor.read_humidity()
		humidity = round(humidity, 3)
		temperature = round(temperature, 3)
		print(u"Temperature: {:g}\u00b0C, Humidity: {:g}%".format(temperature, humidity))
		sensor_data['temperature'] = temperature
		sensor_data['humidity'] = humidity

		# Sending humidity and temperature data to ThingsBoard
		client.publish('kitchen/sensors/temperature', temperature , 1)
		client.publish('kitchen/sensors/humidity', humidity , 1)

		next_reading += INTERVAL
		sleep_time = next_reading-time.time()
		if sleep_time > 0:
			time.sleep(sleep_time)
except KeyboardInterrupt:
	pass

client.loop_stop()
client.disconnect()
