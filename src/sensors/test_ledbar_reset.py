import RPi.GPIO as GPIO
import time
from grove.adc import ADC

# --------------------------
# CONFIGURACION DE PINES
# --------------------------
DATA_PIN = 22
CLOCK_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)

# --------------------------
# FUNCIONES PARA EL LED BAR
# --------------------------

# Enviar 8 bits al LED Bar (protocolo correcto)
def send_8bit(data):
    for i in range(8):
        bit = 1 if (data & 0x80) else 0
        GPIO.output(DATA_PIN, bit)
        GPIO.output(CLOCK_PIN, GPIO.LOW)
        time.sleep(0.00001)
        GPIO.output(CLOCK_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        data <<= 1

# Latch necesario para que el LED Bar actualice la salida
def latch():
    GPIO.output(DATA_PIN, GPIO.LOW)
    time.sleep(0.0001)
    for i in range(8):
        GPIO.output(DATA_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(DATA_PIN, GPIO.LOW)
        time.sleep(0.00001)

# Comando del LED Bar
CMD_MODE = 0x00  # establecer niveles manualmente


# --------------------------
# FUNCIONES LED BAR
# --------------------------

def clear_bar():
    send_8bit(CMD_MODE)
    for _ in range(10):
        send_8bit(0x00)
    latch()

def set_bar_level(level):
    send_8bit(CMD_MODE)
    for i in range(10):
        if i < level:
            send_8bit(0x01)  # encender solo 1 LED por nivel
        else:
            send_8bit(0x00)
    latch()

# --------------------------
# SENSOR DE RUIDO
# --------------------------

adc = ADC()

def readNoise():
    return adc.read(4)

def noiseLevel():
    value = readNoise()
    if value < 100:
        return "Low"
    elif value < 350:
        return "Medium"
    else:
        return "High"

# --------------------------
# TESTS DEL LED BAR
# --------------------------

print("Apagando todos los LEDs...")
clear_bar()
time.sleep(1)

print("Test 1: Encendiendo LEDs uno por uno...")
for i in range(1, 11):
    print(f" Encendiendo LED {i}")
    set_bar_level(i)
    time.sleep(0.5)

print("Test 2: Barra VU-Meter (crecimiento)...")
for i in range(0, 11):
    value = (1 << i) - 1  # 1, 3, 7, 15... estilo barra
    send_8bit(CMD_MODE)
    for n in range(10):
        if n < i:
            send_8bit(value & 0xFF)
        else:
            send_8bit(0x00)
    latch()
    time.sleep(0.5)

print("Apagando...")
clear_bar()

GPIO.cleanup()
print("Test completado.")
