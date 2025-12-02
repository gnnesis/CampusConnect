import time
import sys
import os 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sensors'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'display'))

from TemperatureHumiditySensor import readTemperatureHumidity
from NoiseSensor import noiseLevel
from AirQualitySensor import airQuality
from UltrasonicSensor import arePeople
from LedBarActuator import showStatus
from LcdDisplay import updateLcd

while True:
	temp, hum = readTemperatureHumidity()
	noise = noiseLevel()
	airStatus = airQuality()
	people = arePeople()

	if airStatus == "Bad" or noise == "High" or people:
		showStatus("Red")
	elif airStatus == "Medium" or noise == "Regular":
		showStatus("Yellow")
	else:
		showStatus("Green")

	updateLcd(f"T: {temp:.1f}C", f"H: {hum:.1f}%")

	time.sleep(1)
