import RPi.GPIO as GPIO
import time

class MY9221:
    def __init__(self, data_pin, clock_pin):
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.current_state = None  # Estado actual: 'Low', 'Medium', 'High'
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.output(self.data_pin, GPIO.LOW)
        GPIO.output(self.clock_pin, GPIO.LOW)

    def send_16bit(self, bit_on):
        """Envía un solo bit al LED: True = encender, False = apagar"""
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

    def set_level_by_color(self, state):
        if state == self.current_state:
            return

        self.clear_all()
        time.sleep(0.05)

        for i in range(10):
            # Convertir al índice físico del LED
            led_index = 9 - i  # MY9221 envía primero LED10

            if state == "Low":
                bit_on = led_index >= 2   # LED 3–10
            elif state == "Medium":
                bit_on = led_index >= 1   # LED 2–10
            elif state == "High":
                bit_on = True             # LED 1–10
            else:
                bit_on = False

            self.send_16bit(bit_on)

        self.latch_data()
        self.current_state = state


# Crear instancia de la barra LED
ledBar = MY9221(22, 23)

def showNoiseLevel(noise_status):
    """Actualiza la barra LED según el nivel de ruido con colores físicos"""
    ledBar.set_level_by_color(noise_status)
