# server_backend.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
from datetime import datetime, timezone
import random
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# =========================
# CONFIGURACIÓN
# =========================
INFLUX_URL = "http://localhost:8087"
INFLUX_TOKEN = "vrAK4VDblEmBWNreJJF2oY65lGGaJcuKTVxWui087dDGEYH7zVV64QXlNjEKA0mILZ4_yOxHlUh2op4G9lgNVA=="
INFLUX_ORG = "deusto"
INFLUX_BUCKET = "campusconnect"

# =========================
# Cliente InfluxDB
# =========================
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

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
# Guardar en InfluxDB
# =========================
def save_to_influx(data: dict):
    try:
        p = Point("sensor_reading") \
            .tag("sensor_id", str(data.get("sensor_id", "unknown"))) \
            .tag("category", str(data.get("category", "unknown"))) \
            .tag("noise_level", str(data.get("noise_level", "unknown"))) \
            .tag("air_status", str(data.get("air_status", "unknown")))

        # Fields numéricos / booleanos
        if data.get("temperature") is not None:
            p = p.field("temperature", float(data["temperature"]))
        if data.get("humidity") is not None:
            p = p.field("humidity", float(data["humidity"]))
        if data.get("noise") is not None:
            p = p.field("noise", int(data["noise"]))
        if data.get("air_quality") is not None:
            p = p.field("air_quality", int(data["air_quality"]))
        if data.get("people_present") is not None:
            p = p.field("people_present", bool(data["people_present"]))
        if data.get("distance") is not None:
            p = p.field("distance", float(data["distance"]))

        # Localización
        loc = data.get("location", {})
        if isinstance(loc, dict):
            if loc.get("lat") is not None:
                p = p.field("latitude", float(loc["lat"]))
            if loc.get("lon") is not None:
                p = p.field("longitude", float(loc["lon"]))

        # Timestamp UTC correcto (sin warnings)
        p = p.time(datetime.now(timezone.utc))

        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)
        print(f"📊 Escrito en Influx: {data.get('sensor_id')}")

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
# Hilo automático
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
    return jsonify(sensor_data)

@app.route('/api/sensor-data', methods=['POST'])
def post_sensor_data():
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
