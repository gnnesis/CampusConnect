import time
import sys
import os 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sensors'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'display'))

from TemperatureHumiditySensor import readTemperatureHumidity
from NoiseSensor import noiseLevel
from NoiseSensor import readNoise
from AirQualitySensor import airQuality
from UltrasonicSensor import arePeople
from LedBarActuator import showNoiseLevel
from LcdDisplay import updateLcd

while True:
	temp, hum = readTemperatureHumidity()
	noiseValue = readNoise()
	noiseStatus = noiseLevel()
	airStatus = airQuality()
	people = arePeople()

	showNoiseLevel(noiseStatus)

	updateLcd(f"T: {temp:.1f}C N: {noiseValue}", f"H: {hum:.1f}%")

	time.sleep(1)
