from seeed_dht import DHT

th = DHT('11', 26)

def readTemperatureHumidity():
	hum, temp = th.read()
	return temp, hum
