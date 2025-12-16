from flask import Flask, jsonify
from flask_cors import CORS
from influxdb import InfluxDBClient
from datetime import datetime, timezone
import time
import requests

from seeed_dht import DHT
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.adc import ADC

INFLUX_DB = "campusconnect"
MEASUREMENT = "sensor_data"

DHT_TYPE = "11"
DHT_PORT = 26
ULTRASONIC_PORT = 24
NOISE_ADC_CHANNEL = 4
AIR_ADC_CHANNEL =2

DEFAULT_LAT = 43.2683
DEFAULT_LON = -2.9469

client = InfluxDBClient(host="localhost", port=8086)
client.create_database(INFLUX_DB)
client.switch_database(INFLUX_DB)
print(f"Connected to InfluxDB → DB: {INFLUX_DB}")

print("Initializing Grove sensors...")

dht_sensor = DHT(DHT_TYPE, DHT_PORT)
ultrasonic = GroveUltrasonicRanger(ULTRASONIC_PORT)
adc = ADC()

print("Grove sensors initialized")

def read_real_sensors():
    hum, temp = dht_sensor.read()
    if temp is None or hum is None:
        temp, hum = 0.0, 0.0

    distance_cm = ultrasonic.get_distance()
    distance_m = round(distance_cm / 100.0, 2)

    noise_raw = adc.read(NOISE_ADC_CHANNEL)

    if noise_raw < 100:
        noise_level = "Low"
    elif noise_raw < 350:
        noise_level = "Medium"
    else:
        noise_level = "High"

    air_raw = adc.read(AIR_ADC_CHANNEL)

    if air_raw < 200:
        air_status = "Good"
    elif air_raw < 400:
        air_status = "Regular"
    else:
        air_status = "Bad"

    people_present = 1 if noise_raw > 150 else 0

    now_iso = datetime.now(timezone.utc).isoformat()

    data = {
        "sensor_id": "raspi_grove_01",
        "temperature": float(temp),
        "humidity": float(hum),
        "distance": float(distance_m),
        "noise": int(noise_raw),
        "noise_level": noise_level,
        "air_quality": int(air_raw),
        "air_status": air_status,
        "people_present": people_present,
        "lat": DEFAULT_LAT,
        "lon": DEFAULT_LON,
        "timestamp": now_iso
    }

    return data

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
    print("Saved in InfluxDB:", data["timestamp"])

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

@app.route("/api/weather", methods=["GET"])
def api_weather():
    try:
        API_KEY = "896495917daa8630f381e00643a2363c"
        lat = 43.2683
        lon = -2.9469

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=es"
        res = requests.get(url).json()

        data = {
            "temperature": res["main"]["temp"],
            "temp_max": res["main"]["temp_max"],
            "temp_min": res["main"]["temp_min"],
            "humidity": res["main"]["humidity"],
            "feels_like": res["main"]["feels_like"],
            "weather_desc": res["weather"][0]["description"],
            "rain_probability": res.get("rain", {}).get("1h", 0),
            "wind_speed": res["wind"]["speed"]
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting CampusConnect Backend REAL (Grove + InfluxDB)")
    app.run(host="0.0.0.0", port=5001, debug=True)
