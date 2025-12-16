from grove.adc import ADC

adc = ADC()

def readNoise():
	return adc.read(4)