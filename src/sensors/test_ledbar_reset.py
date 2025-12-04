import RPi.GPIO as GPIO
import time
from grove.adc import ADC

DATA_PIN = 22
CLOCK_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)

# --------------------------
# LOW-LEVEL FUNCTIONS
# --------------------------

def send_8bit(data):
    for i in range(8):
        bit = 1 if (data & 0x80) else 0
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

CMD_MODE = 0x00

def clear_bar():
    send_8bit(CMD_MODE)
    for _ in range(10):
        send_8bit(0x00)
    latch()

# --------------------------
# TEST: LED por LED con FADING
# --------------------------

print("🔥 Test: encendiendo los 10 LEDs uno por uno con intensidad creciente...")

clear_bar()
time.sleep(0.5)

for led in range(10):

    print(f" Encendiendo LED {led+1} con fade...")

    # Fade de intensidad → 5 pasos
    for intensity in [0x01, 0x03, 0x07, 0x0F, 0x1F]:

        send_8bit(CMD_MODE)

        for i in range(10):
            if i == led:
                send_8bit(intensity)   # brillo creciente
            else:
                send_8bit(0x00)

        latch()
        time.sleep(0.08)

# Esperar un momento al final
time.sleep(1)

clear_bar()
GPIO.cleanup()
print("✨ Test completado correctamente.")
