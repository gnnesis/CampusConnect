import time
import sys
import os 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sensors'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'display'))

from TemperatureHumiditySensor import readTemperatureHumidity
from NoiseSensor import readNoise
from AirQualitySensor import readAirQuality
from UltrasonicSensor import arePeople
from LedBarActuator import showStatus
from LcdDisplay import updateLcd

while True:
	temp, hum = readTemperatureHumidity()
	noise = readNoise()
	airQuality = readAirQuality()
	people = arePeople()

	if airQuality == "Bad" or noise == "High" or people:
		showStatus("Red")
	elif airQuality == "Medium" or noise == "Regular":
		showStatus("Yellow")
	else:
		showStatus("Green")

	updateLcd(f"T: {temp:.1f}ºC R: {noise}", f"air: {airQuality}")

	time.sleep(1)
