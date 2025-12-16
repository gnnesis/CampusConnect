import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sensors'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'display'))

from TemperatureHumiditySensor import readTemperatureHumidity
from NoiseSensor import readNoise
from AirQualitySensor import airQuality
from UltrasonicSensor import arePeople
from LedBarActuator import showNoiseLevel
from LcdDisplay import updateLcd

LOW_THRESHOLD = 100
MEDIUM_THRESHOLD = 350
HYSTERESIS = 10  

current_noise_state = None

def get_noise_state(value, current_state):
    if current_state == "Low":
        if value > LOW_THRESHOLD + HYSTERESIS:
            return "Medium"
        else:
            return "Low"
    elif current_state == "Medium":
        if value < LOW_THRESHOLD - HYSTERESIS:
            return "Low"
        elif value > MEDIUM_THRESHOLD + HYSTERESIS:
            return "High"
        else:
            return "Medium"
    elif current_state == "High":
        if value < MEDIUM_THRESHOLD - HYSTERESIS:
            return "Medium"
        else:
            return "High"
    else:
        if value < LOW_THRESHOLD:
            return "Low"
        elif value < MEDIUM_THRESHOLD:
            return "Medium"
        else:
            return "High"

try:
    while True:
        temp, hum = readTemperatureHumidity()
        noise_value = readNoise()
        air_status = airQuality()
        people = arePeople()

        current_noise_state = get_noise_state(noise_value, current_noise_state)
        
        showNoiseLevel(current_noise_state)
        updateLcd(f"T: {temp:.1f}C", f"H: {hum:.1f}%")

        time.sleep(5)

except KeyboardInterrupt:
    print("\nProgram stopped by user")