import RPi.GPIO as GPIO
import time

class MY9221:
    def __init__(self, data_pin, clock_pin):
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.current_level = -1  # Nivel actual de LEDs
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.output(self.data_pin, GPIO.LOW)
        GPIO.output(self.clock_pin, GPIO.LOW)

    def send_16bit(self, bit_on):
        """
        Envia un solo bit a la barra.
        bit_on: True para encender, False para apagar
        """
        GPIO.output(self.data_pin, GPIO.HIGH if bit_on else GPIO.LOW)
        GPIO.output(self.clock_pin, GPIO.LOW)
        time.sleep(0.00001)
        GPIO.output(self.clock_pin, GPIO.HIGH)
        time.sleep(0.00001)

    def latch_data(self):
        GPIO.output(self.data_pin, GPIO.LOW)
        time.sleep(0.0001)
        for _ in range(8):
            GPIO.output(self.data_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.data_pin, GPIO.LOW)
            time.sleep(0.00001)

    def clear_all(self):
        for _ in range(10):
            self.send_16bit(False)
        self.latch_data()

    def set_level(self, level):
        """
        Enciende solo los primeros 'level' LEDs y apaga el resto.
        Solo actualiza si cambia el nivel.
        """
        if level == self.current_level:
            return  # No hacer nada si no hay cambio

        # Apagar todo brevemente
        self.clear_all()
        time.sleep(0.1)

        # Enciende los primeros 'level' LEDs
        for i in range(10):
            self.send_16bit(i < level)
        self.latch_data()
        self.current_level = level


# Crear instancia de la barra LED
ledBar = MY9221(22, 23)

def showNoiseLevel(noise_status):
    """
    Actualiza la barra LED según el nivel de ruido:
    Low: 3 LEDs
    Medium: 6 LEDs
    High: 10 LEDs
    """
    if noise_status == "Low":
        ledBar.set_level(3)
    elif noise_status == "Medium":
        ledBar.set_level(6)
    elif noise_status == "High":
        ledBar.set_level(10)
    else:
        ledBar.set_level(0)
