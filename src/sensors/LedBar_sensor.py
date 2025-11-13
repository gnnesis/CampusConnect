# led_bar_controller.py
import RPi.GPIO as GPIO

class LedBar:
    def __init__(self, pin=16, freq=1000):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, freq)
        self.pwm.start(0)

    def update(self, noise_level):
        """
        Ajusta brillo según ruido
        """
        if noise_level < 40:
            duty_cycle = 30
            level = "Low"
        elif noise_level < 60:
            duty_cycle = 60
            level = "Medium"
        else:
            duty_cycle = 100
            level = "High"

        self.pwm.ChangeDutyCycle(duty_cycle)
        print(f"Noise: {noise_level} dB → LED bar: {level}, Brightness: {duty_cycle}%")

    def cleanup(self):
        self.pwm.stop()
