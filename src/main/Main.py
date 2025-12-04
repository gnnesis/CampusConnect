import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sensors'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'display'))

from TemperatureHumiditySensor import readTemperatureHumidity
from NoiseSensor import noiseLevel, readNoise
from AirQualitySensor import airQuality
from UltrasonicSensor import arePeople
from LedBarActuator import showNoiseLevel
from LcdDisplay import updateLcd

# Umbrales con histeresis
LOW_THRESHOLD = 100
MEDIUM_THRESHOLD = 350
HYSTERESIS = 10  # Evita cambios constantes si está cerca del límite

current_noise_state = None

def get_noise_state(value, current_state):
    """
    Devuelve el estado 'Low', 'Medium' o 'High' usando histeresis
    """
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
        # Estado inicial
        if value < LOW_THRESHOLD:
            return "Low"
        elif value < MEDIUM_THRESHOLD:
            return "Medium"
        else:
            return "High"


while True:
    temp, hum = readTemperatureHumidity()
    noise_value = readNoise()
    air_status = airQuality()
    people = arePeople()

    # Determinar el estado de ruido estable
    current_noise_state = get_noise_state(noise_value, current_noise_state)

    # Actualizar barra LED solo si cambia el estado
    showNoiseLevel(current_noise_state)

    # Actualizar LCD
    updateLcd(f"T: {temp:.1f}C N: {noise_value}", f"H: {hum:.1f}%")

    time.sleep(1)
