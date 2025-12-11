# ============================================
#  CAMPUSCONNECT BACKEND REAL + INFLUXDB 1.x
#  Raspberry Pi + Grove Base Hat
# ============================================

from flask import Flask, jsonify
from flask_cors import CORS
from influxdb import InfluxDBClient
from datetime import datetime, timezone
import time

# Grove librerías
from seeed_dht import DHT
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_sound_sensor import GroveSoundSensor
from grove.grove_air_quality_sensor_v1_3 import GroveAirQualitySensorV1_3

# =========================
# CONFIG
# =========================
INFLUX_DB = "campusconnect"
MEASUREMENT = "sensor_data"

# PUERTOS GROVE (AJÚSTALOS SI LOS TIENES EN OTROS)
DHT_TYPE = "11"          # "11" = DHT11, "22" = DHT22
DHT_PORT = 5             # D5 en el Grove Base Hat
ULTRASONIC_PORT = 16     # D16
SOUND_PORT = 18          # D18
AIR_QUALITY_PORT = 0     # A0

DEFAULT_LAT = 43.2683
DEFAULT_LON = -2.9469

# =========================
# INFLUXDB
# =========================
client = InfluxDBClient(host="localhost", port=8086)
client.create_database(INFLUX_DB)
client.switch_database(INFLUX_DB)
print(f"✅ Conectado a InfluxDB → DB: {INFLUX_DB}")

# =========================
# INICIALIZAR SENSORES
# =========================
print("🔌 Inicializando sensores Grove...")

dht_sensor = DHT(DHT_TYPE, DHT_PORT)
ultrasonic = GroveUltrasonicRanger(ULTRASONIC_PORT)
sound_sensor = GroveSoundSensor(SOUND_PORT)
air_sensor = GroveAirQualitySensorV1_3(AIR_QUALITY_PORT)

print("✅ Sensores Grove inicializados")

# =========================
# LECTURA REAL DE SENSORES
# =========================
def read_real_sensors():
    # Temperatura y humedad
    temp, hum = dht_sensor.read()
    if temp is None or hum is None:
        temp, hum = 0.0, 0.0

    # Distancia (cm → m)
    distance_cm = ultrasonic.get_distance()
    distance_m = round(distance_cm / 100.0, 2)

    # Ruido
    sound_raw = sound_sensor.sound
    if sound_raw < 100:
        noise_level = "Low"
    elif sound_raw < 300:
        noise_level = "Medium"
    else:
        noise_level = "High"

    # Calidad del aire
    air_raw = air_sensor.MQ_percentage["SMOKE"]
    air_quality = int(air_raw)

    if air_quality < 100:
        air_status = "Good"
    elif air_quality < 300:
        air_status = "Regular"
    else:
        air_status = "Bad"

    # Presencia (ejemplo simple)
    people_present = 1 if sound_raw > 80 else 0

    now_iso = datetime.now(timezone.utc).isoformat()

    data = {
        "sensor_id": "raspi_grove_01",
        "temperature": float(temp),
        "humidity": float(hum),
        "distance": float(distance_m),
        "noise": int(sound_raw),
        "noise_level": noise_level,
        "air_quality": air_quality,
        "air_status": air_status,
        "people_present": people_present,
        "lat": DEFAULT_LAT,
        "lon": DEFAULT_LON,
        "timestamp": now_iso
    }

    return data

# =========================
# GUARDAR EN INFLUXDB
# =========================
def save_to_influx(data):
    json_body = [{
        "measurement": MEASUREMENT,
        "tags": {
            "sensor_id": data["sensor_id"],
            "noise_level": data["noise_level"],
            "air_status": data["air_status"]
        },
        "time": data["timestamp"],
        "fields": {
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "distance": data["distance"],
            "noise": data["noise"],
            "air_quality": data["air_quality"],
            "people_present": data["people_present"],
            "lat": data["lat"],
            "lon": data["lon"]
        }
    }]
    client.write_points(json_body)
    print("💾 Guardado en InfluxDB:", data["timestamp"])

# =========================
# FLASK API
# =========================
app = Flask(__name__)
CORS(app)

@app.route("/api/sensors", methods=["GET"])
def api_sensors():
    data = read_real_sensors()
    save_to_influx(data)
    return jsonify(data)

@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({"status": "ok", "time": datetime.now(timezone.utc).isoformat()})

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("🚀 Iniciando CampusConnect Backend REAL (Grove + InfluxDB)")
    app.run(host="0.0.0.0", port=5001, debug=True)
