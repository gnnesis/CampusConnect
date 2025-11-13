# noise_sensor.py
import RPi.GPIO as GPIO

class NoiseSensor:
    def __init__(self, pin=18):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def read_noise_level(self):
        """
        Retorna nivel de ruido simulado o real
        Digital: 0 = silencio, 1 = ruido alto
        """
        value = GPIO.input(self.pin)
        if value == 0:
            return 30  # silencioso
        else:
            return 70  # ruido alto
