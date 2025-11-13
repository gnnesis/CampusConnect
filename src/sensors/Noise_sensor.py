import RPi.GPIO as GPIO

class NoiseSensor:
    def __init__(self, pin=18):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
    
    def read_noise(self):
        """
        Devuelve True si hay ruido, False si poco ruido.
        """
        return GPIO.input(self.pin)
    
    def cleanup(self):
        GPIO.cleanup()
