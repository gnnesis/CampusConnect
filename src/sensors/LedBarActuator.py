import RPi.GPIO as GPIO
import time

class MY9221:
    def __init__(self, data_pin, clock_pin):
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.current_level = -1
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
        self.send_16bit(0x0000)
        for i in range(10):
            self.send_16bit(0x0000)
        self.latch_data()
    
    def set_level(self, level):
        # Evitar sobreposición
        if level == self.current_level:
            return
        self.clear_all()
        time.sleep(0.05)
        self.send_16bit(0x0000)
        for i in range(10):
            if i < level:
                self.send_16bit(0xFFFF)
            else:
                self.send_16bit(0x0000)
        self.latch_data()
        self.current_level = level

# Crear instancia
ledBar = MY9221(22, 23)

# Función para mostrar el nivel de ruido
def showNoiseLevel(noise_status):
    if noise_status == "Low":
        ledBar.set_level(3)
    elif noise_status == "Medium":
        ledBar.set_level(6)
    elif noise_status == "High":
        ledBar.set_level(10)
    else:
        ledBar.set_level(0)
