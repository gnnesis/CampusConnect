from grove.grove_temperature_humidity_sensor import DHT
th = DHT("11", 26)

def readTemperatureHumidity():
	hum, temp = th.read()
	return temp, hum
