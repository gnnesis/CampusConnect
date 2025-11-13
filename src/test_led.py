import RPi.GPIO as GPIO
import time

LED_PIN = 16  # tu pin PWM donde está conectada la LED bar

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Crear PWM
pwm = GPIO.PWM(LED_PIN, 1000)  # frecuencia 1kHz
pwm.start(0)  # brillo inicial 0%

try:
    # Probar varios niveles de brillo
    for duty in [0, 30, 60, 100, 0]:
        pwm.ChangeDutyCycle(duty)
        print("Brillo:", duty)
        time.sleep(1)

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO limpiado, prueba terminada")
