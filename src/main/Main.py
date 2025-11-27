import time
from TemperatureHumiditySensor import readTemperatureHumidity
from NoiseSensor import readNoise
from AirQualitySensor import readAirQuality
from UltrasonicSensor import arePeople

while True:
	temp, hum = readTemperatureHumidity()
	noise = readNoise()
	airQuality = readAirQuality()
	people = arePeople

	if airQuality == "Bad" or noise == "High" or people:
		showStatus("Red")
	elif airQuality == "Medium" or air == "Regular":
		showStatus("Yellow")
	else:
		showStatus("Green")

	updateLcd(f"T: {temp:.1f}ºC R: {noise}", f"air: {airQuality}")

	time.sleep(1)
