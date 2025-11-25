from grove.adc import ADC
adc = ADC()

def readAirQuality():
	return adc.read(2)

def airQuality():
	value = readAirQuality()
	if value < 200:
		return "Good"
	elif value < 400:
		return "Regular"
	else:
		return "Bad"
