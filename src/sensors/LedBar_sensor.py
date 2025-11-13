# sensors/led_bar_controller.py
import RPi.GPIO as GPIO

class LedBar:
    def __init__(self, pin=16, freq=1000):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, freq)
        self.pwm.start(0)

    def update(self, noise_level):
        """
        Ajusta brillo de la LED bar según el nivel de ruido
        """
        if noise_level < 40:
            duty_cycle = 30
            level = "Low"
        elif noise_level < 60:
            duty_cycle = 60
            level = "Medi
