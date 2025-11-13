import RPi.GPIO as GPIO
import time

# Pin donde está conectado el sensor de ruido
NOISE_PIN = 18

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(NOISE_PIN, GPIO.IN)

print("Probando sensor de ruido. Pulsa Ctrl+C para salir...")

try:
    while True:
        # Leer valor digital del sensor: 0 = silencio, 1 = ruido
        value = GPIO.input(NOISE_PIN)
        
        if value == 0:
            noise_level = 30  # nivel bajo aproximado en dB
        else:
            noise_level = 70  # nivel alto aproximado en dB
        
        print(f"Nivel de ruido: {noise_level} dB")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Prueba finalizada. Limpiando GPIO...")
    GPIO.cleanup()
