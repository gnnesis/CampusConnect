import RPi.GPIO as GPIO
import time

class MY9221:
    def __init__(self, data_pin, clock_pin):
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.current_state = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.output(self.data_pin, GPIO.LOW)
        GPIO.output(self.clock_pin, GPIO.LOW)

    def send_16bit(self, value):
        for i in range(16):
            bit = (value >> (15 - i)) & 1
            GPIO.output(self.data_pin, GPIO.HIGH if bit else GPIO.LOW)
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
        for _ in range(5):
            self.send_16bit(0x0000)
        self.latch_data()

    def set_level_by_color(self, state):
        if state == self.current_state:
            return

        self.clear_all()
        time.sleep(0.05)

        for channel in range(5, 0, -1):
            pysical_channel = 6 - channel
            if state == "Low":
                bit_on = pysical_channel >= 2
            elif state == "Medium":
                bit_on = pysical_channel >= 1
            elif state == "High":
                bit_on = True
            else:
                bit_on = False

            self.send_16bit(0xFFFF if bit_on else 0x0000)

        self.latch_data()
        self.current_state = state

ledBar = MY9221(22, 23)

def showNoiseLevel(noise_status):
    ledBar.set_level_by_color(noise_status)