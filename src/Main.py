# main.py
import RPi.GPIO as GPIO
import time
from sensors.noise_sensor import NoiseSensor
from sensors.led_bar_controller import LedBar

GPIO.setmode(GPIO.BCM)

# Crear instancias
noise_sensor = NoiseSensor(pin=18)
led_bar = LedBar(pin=16)

try:
    while True:
        noise = noise_sensor.read_noise_level()
        led_bar.update(noise)
        time.sleep(1)

except KeyboardInterrupt:
    print("Saliendo… limpiando GPIO")
    led_bar.cleanup()
    GPIO.cleanup()
