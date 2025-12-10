# server_backend.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
from datetime import datetime, timezone
import random
from influxdb import InfluxDBClient

# =========================
# CONFIGURACIÓN INFLUXDB 1.8
# =========================
INFLUX_HOST = "localhost"
INFLUX_PORT = 8087          # puerto de InfluxDB
INFLUX_DB = "campusconnect" # tu base de datos
INFLUX_USER = "admin"       # tu usuario
INFLUX_PASSWORD = "admin123" # tu contraseña

# =========================
# Cliente InfluxDB 1.x
# =========================
client = InfluxDBClient(
    host=INFLUX_HOST,
    port=INFLUX_PORT,
    username=INFLUX_USER,
    password=INFLUX_PASSWORD,
    database=INFLUX_DB
)

# Crear base de datos si no existe
databases = [db['name'] for db in client.get_list_database()]
if INFLUX_DB not in databases:
    client.create_database(INFLUX_DB)
    print(f"✅ Base de datos '{INFLUX_DB}' creada")

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

# =========================
# Función para guardar datos en InfluxDB 1.x
# =========================
def save_to_influx(data):
    try:
        json_body = [
            {
                "measurement": "sensor_reading",
                "tags": {
                    "sensor_id": data.get("sensor_id", "unknown"),
                    "category": data.get("category", "unknown"),
                    "noise_level": data.get("noise_level", "unknown"),
                    "air_status": data.get("air_status", "unknown")
                },
                "time": datetime.now(timezone.utc).isoformat(),
                "fields": {
                    "temperature": float(data.get("temperature", 0)),
                    "humidity": float(data.get("humidity", 0)),
                    "noise": int(data.get("noise", 0)),
                    "air_quality": int(data.get("air_quality", 0)),
                    "people_present": bool(data.get("people_present", False)),
                    "distance": float(data.get("distance", 0)),
                    "latitude": float(data.get("location", {}).get("lat", 0)),
                    "longitude": float(data.get("location", {}).get("lon", 0))
                }
            }
        ]
        client.write_points(json_body)
        print(f"📊 Guardado en Influx: {data.get('sensor_id')}")
        return True
    except Exception as e:
        print(f"❌ Error al guardar en Influx: {e}")
        return False

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
# Hilo automático que guarda datos cada N segundos
# =========================
def auto_save_loop(interval=10):
    print(f"🔁 Auto-save thread iniciado: cada {interval}s")
    while True:
        read_sensors_simulated()
        save_to_influx(sensor_data)
        time.sleep(interval)

threading.Thread(target=auto_save_loop, daemon=True).start()

# =========================
# Endpoints
# =========================
@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    """Devuelve el estado actual de los sensores"""
    return jsonify(sensor_data)

@app.route('/api/sensor-data', methods=['POST'])
def post_sensor_data():
    """Recibe JSON y lo guarda en InfluxDB"""
    data = request.get_json(force=True)
    data["timestamp"] = datetime.now(timezone.utc).isoformat()
    ok = save_to_influx(data)
    return jsonify({"status": "success" if ok else "error"})

# =========================
# Main
# =========================
if __name__ == '__main__':
    print("🚀 Iniciando CampusConnect Backend")
    app.run(host='0.0.0.0', port=5001, debug=True)
