import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sensors'))

import RPi.GPIO as GPIO
import time

# Configuración
DATA_PIN = 22
CLOCK_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)

def send_16bit(data):
    for i in range(16):
        bit = 1 if (data & 0x8000) else 0
        GPIO.output(DATA_PIN, bit)
        GPIO.output(CLOCK_PIN, GPIO.LOW)
        time.sleep(0.00001)
        GPIO.output(CLOCK_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        data <<= 1

def latch():
    GPIO.output(DATA_PIN, GPIO.LOW)
    time.sleep(0.0001)
    for i in range(8):
        GPIO.output(DATA_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(DATA_PIN, GPIO.LOW)
        time.sleep(0.00001)

print("Apagando todos los LEDs...")
send_16bit(0x0000)
for i in range(10):
    send_16bit(0x0000)
latch()
time.sleep(2)

print("Test: Encendiendo LEDs uno por uno...")
for level in range(1, 11):
    print(f"Encendiendo {level} LED(s)")
    send_16bit(0x0000)
    for i in range(10):
        if i < level:
            send_16bit(0xFFFF)
        else:
            send_16bit(0x0000)
    latch()
    time.sleep(1)

print("Apagando todo...")
send_16bit(0x0000)
for i in range(10):
    send_16bit(0x0000)
latch()

GPIO.cleanup()
print("Test completado")