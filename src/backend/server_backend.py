# server_backend.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
from datetime import datetime, timezone
import random

# =========================
# Flask app
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# Estado global de sensores (simulado)
# =========================
sensor_data = {
    "sensor_id": "sensor_01",
    "category": "environment",
    "temperature": 22.5,
    "humidity": 65.0,
    "noise": 150,
    "noise_level": "Medium",
    "air_quality": 250,
    "air_status": "Good",
    "people_present": True,
    "distance": 45.5,
    "location": {"lat": 43.2683, "lon": -2.9469},
    "timestamp": datetime.now(timezone.utc).isoformat()
}

weather_data = {
    "temperature": 21.5,
    "temp_max": 23.0,
    "temp_min": 20.0,
    "weather_desc": "Soleado",
    "weather_main": "clear",
    "rain_probability": 10,
    "humidity": 55,
    "wind_speed": 5.2,
    "feels_like": 21.0
}

# =========================
# Simulación de sensores
# =========================
def read_sensors_simulated():
    sensor_data["temperature"] = round(20 + random.uniform(-3, 5), 1)
    sensor_data["humidity"] = round(60 + random.uniform(-10, 15), 1)
    sensor_data["noise"] = int(100 + random.uniform(-50, 300))

    if sensor_data["noise"] < 100:
        sensor_data["noise_level"] = "Low"
    elif sensor_data["noise"] < 350:
        sensor_data["noise_level"] = "Medium"
    else:
        sensor_data["noise_level"] = "High"

    sensor_data["air_quality"] = int(150 + random.uniform(-50, 250))
    if sensor_data["air_quality"] < 200:
        sensor_data["air_status"] = "Good"
    elif sensor_data["air_quality"] < 400:
        sensor_data["air_status"] = "Regular"
    else:
        sensor_data["air_status"] = "Bad"

    sensor_data["people_present"] = random.choice([True, False, True])
    sensor_data["distance"] = round(random.uniform(20, 150), 1)
    sensor_data["location"] = {
        "lat": 43.2683 + random.uniform(-0.0005, 0.0005),
        "lon": -2.9469 + random.uniform(-0.0005, 0.0005)
    }
    sensor_data["timestamp"] = datetime.now(timezone.utc).isoformat()

# =========================
# Hilo automático que actualiza sensores cada 10s
# =========================
def auto_update_loop(interval=10):
    print(f"🔁 Sensor simulation thread iniciado: cada {interval}s")
    while True:
        read_sensors_simulated()
        time.sleep(interval)

threading.Thread(target=auto_update_loop, daemon=True).start()

# =========================
# Endpoints
# =========================
@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    return jsonify(sensor_data)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    # Actualizar clima simulado aleatorio para que cambie un poco
    weather_data["temperature"] = round(20 + random.uniform(-3, 5), 1)
    weather_data["temp_max"] = weather_data["temperature"] + random.uniform(0, 3)
    weather_data["temp_min"] = weather_data["temperature"] - random.uniform(0, 3)
    weather_data["humidity"] = int(50 + random.uniform(-10, 20))
    weather_data["wind_speed"] = round(2 + random.uniform(0, 5), 1)
    weather_data["feels_like"] = weather_data["temperature"] - random.uniform(0, 2)
    return jsonify(weather_data)

# =========================
# Main
# =========================
if __name__ == '__main__':
    print("🚀 Iniciando CampusConnect Backend")
    app.run(host='0.0.0.0', port=5001, debug=True)
