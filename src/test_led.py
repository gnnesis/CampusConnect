# test_led.py
import RPi.GPIO as GPIO
import time
from sensors.led_bar_controller import LedBar

GPIO.setmode(GPIO.BCM)
led = LedBar(pin=16)

try:
    for level in [0, 30, 60, 100, 0]:
        led.pwm.ChangeDutyCycle(level)
        print("Brillo:", level)
        time.sleep(1)
finally:
    led.cleanup()
    GPIO.cleanup()
