import RPi.GPIO as GPIO
import time

class MY9221:
    def __init__(self, data_pin, clock_pin):
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.output(self.data_pin, GPIO.LOW)
        GPIO.output(self.clock_pin, GPIO.LOW)

    def send_16bit(self, data):
        for i in range(16):
            bit = 1 if (data & 0x8000) else 0
            GPIO.output(self.data_pin, bit)
            GPIO.output(self.clock_pin, GPIO.LOW)
            time.sleep(0.00001)
            GPIO.output(self.clock_pin, GPIO.HIGH)
            time.sleep(0.00001)
            data <<= 1

    def latch_data(self):
        GPIO.output(self.data_pin, GPIO.LOW)
        time.sleep(0.0001)
        for i in range(8):
            GPIO.output(self.data_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.data_pin, GPIO.LOW)
            time.sleep(0.00001)

    def clear_all(self):
        for i in range(10):
            self.send_16bit(0x0000)
        self.latch_data()

    def set_level_color(self, level, color):
        """
        level: cantidad de LEDs a encender
        color: 'green', 'yellow', 'red'
        """
        self.clear_all()
        time.sleep(0.05)

        for i in range(10):
            # Mapear LEDs físicos: 0=rojo, 1=amarillo, 2-9=verdes
            if color == 'green' and i >= 2 and i < 2 + level:
                self.send_16bit(0xFFFF)
            elif color == 'yellow' and i == 1 and level >= 1:
                self.send_16bit(0xFFFF)
                level -= 1
            elif color == 'red' and i == 0 and level >= 1:
                self.send_16bit(0xFFFF)
                level -= 1
            else:
                self.send_16bit(0x0000)
        self.latch_data()


# Crear instancia de la barra LED
ledBar = MY9221(22, 23)

def showNoiseLevel(noise_status):
    """
    Muestra el nivel de ruido en la barra LED con colores:
    Low: 3 LEDs verdes
    Medium: 6 LEDs amarillos
    High: 10 LEDs (1 rojo + resto verde)
    """
    if noise_status == "Low":
        # 3 LEDs verdes (LEDs 3,4,5)
        ledBar.set_level_color(3, 'green')
    elif noise_status == "Medium":
        # 6 LEDs: amarillo + verdes
        # LED 2 amarillo + 5 LEDs verdes
        ledBar.set_level_color(6, 'yellow')
    elif noise_status == "High":
        # 10 LEDs: rojo + verdes
        ledBar.set_level_color(10, 'red')
    else:
        ledBar.clear_all()
