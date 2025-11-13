# test_noise.py
import RPi.GPIO as GPIO
import time
from sensors.noise_sensor import NoiseSensor

GPIO.setmode(GPIO.BCM)
sensor = NoiseSensor(pin=18)

try:
    while True:
        noise = sensor.read_noise_level()
        print("Noise level:", noise)
        time.sleep(0.5)
finally:
    GPIO.cleanup()
