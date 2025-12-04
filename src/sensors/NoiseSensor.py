from grove.adc import ADC
adc = ADC()

def readNoise():
	return adc.read(4)

def noiseLevel():
	value = readNoise()
	if value < 100:
		return "Low"
	elif value >= 100 or value < 350:
		return "Medium"
	else:
		return "High"
