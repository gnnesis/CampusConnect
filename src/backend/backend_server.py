from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import sys
import os
import requests
from datetime import datetime
import json

# Importar sensores (comentado si no tienes el hardware)
# sys.path.append(os.path.join(os.path.dirname(__file__), 'sensors'))
# from TemperatureHumiditySensor import readTemperatureHumidity
# from NoiseSensor import noiseLevel, readNoise
# from AirQualitySensor import airQuality, readAirQuality
# from UltrasonicSensor import arePeople, distance

app = Flask(__name__)
CORS(app)

# Configuración OpenWeather
OPENWEATHER_API_KEY = "896495917daa8630f381e00643a2363c"  # Reemplaza con tu API key
OPENWEATHER_LAT = "43.2683"
OPENWEATHER_LON = "-2.9469"

# Estado global de sensores (datos simulados si no hay hardware)
sensor_data = {
    "temperature": 22.5,
    "humidity": 65.0,
    "noise": 150,
    "noise_level": "Medium",
    "air_quality": 250,
    "air_status": "Good",
    "people_present": True,
    "distance": 45.5,
    "location": {"lat": 43.2683, "lon": -2.9469},
    "timestamp": datetime.now().isoformat()
}

weather_data = {
    "temperature": 18.0,
    "temp_max": 22.0,
    "temp_min": 15.0,
    "feels_like": 17.5,
    "humidity": 70,
    "rain_probability": 20,
    "weather_desc": "nubes dispersas",
    "weather_main": "Clouds",
    "wind_speed": 3.5,
    "timestamp": datetime.now().isoformat()
}

# Almacenamiento de datos de sensores
sensor_history = []

def read_sensors_real():
    """Leer sensores reales del hardware"""
    try:
        temp, hum = readTemperatureHumidity()
        noise_value = readNoise()
        air_value = readAirQuality()
        air_status = airQuality()
        people = arePeople()
        dist = distance()
        
        sensor_data["temperature"] = temp
        sensor_data["humidity"] = hum
        sensor_data["noise"] = noise_value
        sensor_data["noise_level"] = noiseLevel()
        sensor_data["air_quality"] = air_value
        sensor_data["air_status"] = air_status
        sensor_data["people_present"] = people
        sensor_data["distance"] = dist
        sensor_data["timestamp"] = datetime.now().isoformat()
        
        return True
    except Exception as e:
        print(f"Error leyendo sensores reales: {e}")
        return False

def read_sensors_simulated():
    """Simular lectura de sensores (para testing sin hardware)"""
    import random
    
    # Simular variaciones realistas
    sensor_data["temperature"] = round(20 + random.uniform(-3, 5), 1)
    sensor_data["humidity"] = round(60 + random.uniform(-10, 15), 1)
    sensor_data["noise"] = int(100 + random.uniform(-50, 300))
    
    # Determinar nivel de ruido
    if sensor_data["noise"] < 100:
        sensor_data["noise_level"] = "Low"
    elif sensor_data["noise"] < 350:
        sensor_data["noise_level"] = "Medium"
    else:
        sensor_data["noise_level"] = "High"
    
    sensor_data["air_quality"] = int(150 + random.uniform(-50, 250))
    
    # Determinar calidad del aire
    if sensor_data["air_quality"] < 200:
        sensor_data["air_status"] = "Good"
    elif sensor_data["air_quality"] < 400:
        sensor_data["air_status"] = "Regular"
    else:
        sensor_data["air_status"] = "Bad"
    
    sensor_data["people_present"] = random.choice([True, False, True])  # 66% probabilidad de personas
    sensor_data["distance"] = round(random.uniform(20, 150), 1)
    sensor_data["timestamp"] = datetime.now().isoformat()

def fetch_weather_data():
    """Obtener datos de OpenWeather"""
    try:
        # Current weather
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={OPENWEATHER_LAT}&lon={OPENWEATHER_LON}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es"
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            print(f"Error en API OpenWeather: {response.status_code}")
            return False
        
        data = response.json()
        
        # Forecast para probabilidad de lluvia
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={OPENWEATHER_LAT}&lon={OPENWEATHER_LON}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es"
        forecast_response = requests.get(forecast_url, timeout=5)
        forecast_data = forecast_response.json()
        
        # Calcular probabilidad de lluvia de las próximas 3 horas
        rain_prob = 0
        if 'list' in forecast_data and len(forecast_data['list']) > 0:
            if 'pop' in forecast_data['list'][0]:
                rain_prob = forecast_data['list'][0]['pop'] * 100
        
        weather_data["temperature"] = data["main"]["temp"]
        weather_data["temp_max"] = data["main"]["temp_max"]
        weather_data["temp_min"] = data["main"]["temp_min"]
        weather_data["feels_like"] = data["main"]["feels_like"]
        weather_data["humidity"] = data["main"]["humidity"]
        weather_data["weather_desc"] = data["weather"][0]["description"]
        weather_data["weather_main"] = data["weather"][0]["main"]
        weather_data["wind_speed"] = data["wind"]["speed"]
        weather_data["rain_probability"] = round(rain_prob)
        weather_data["timestamp"] = datetime.now().isoformat()
        
        return True
        
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return False

@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    """Endpoint para obtener datos de sensores"""
    # Intentar leer sensores reales, si falla usar simulación
    if not read_sensors_real():
        read_sensors_simulated()
    
    return jsonify(sensor_data)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Endpoint para obtener datos del clima"""
    fetch_weather_data()
    return jsonify(weather_data)

@app.route('/api/all', methods=['GET'])
def get_all_data():
    """Endpoint para obtener todos los datos"""
    if not read_sensors_real():
        read_sensors_simulated()
    fetch_weather_data()
    
    return jsonify({
        "sensors": sensor_data,
        "weather": weather_data
    })

@app.route('/api/heatmap', methods=['GET'])
def get_heatmap_data():
    """Endpoint para datos del heatmap"""
    if not read_sensors_real():
        read_sensors_simulated()
    
    # Calcular intensidad para el heatmap (0-1)
    noise_intensity = min(sensor_data["noise"] / 500, 1.0)
    people_intensity = 1.0 if sensor_data["people_present"] else 0.3
    air_intensity = min(sensor_data["air_quality"] / 600, 1.0)
    
    # Combinar intensidades
    combined_intensity = (noise_intensity * 0.4 + 
                         people_intensity * 0.3 + 
                         air_intensity * 0.3)
    
    return jsonify({
        "lat": sensor_data["location"]["lat"],
        "lon": sensor_data["location"]["lon"],
        "intensity": combined_intensity,
        "details": {
            "noise": sensor_data["noise_level"],
            "air": sensor_data["air_status"],
            "people": sensor_data["people_present"],
            "temp": sensor_data["temperature"]
        }
    })

@app.route('/api/sensor-data', methods=['POST'])
def post_sensor_data():
    """Endpoint para recibir datos de sensores externos"""
    try:
        data = request.get_json()
        sensor_history.append({
            **data,
            "timestamp": datetime.now().isoformat()
        })
        return jsonify({"status": "success", "message": "Data received"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/all-data', methods=['GET'])
def get_all_sensor_data():
    """Endpoint para obtener todo el historial de sensores"""
    return jsonify(sensor_history)

@app.route('/api/status', methods=['GET'])
def get_status():
    """Endpoint para verificar estado del servidor"""
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "sensors_connected": False,  # Cambiar a True si tienes hardware
        "weather_api_configured": OPENWEATHER_API_KEY != "TU_API_KEY_AQUI"
    })

@app.route('/', methods=['GET'])
def home():
    """Página de inicio del API"""
    return """
    <h1>🎓 CampusConnect API</h1>
    <p>Backend para el sistema de monitorización del campus</p>
    <h2>Endpoints disponibles:</h2>
    <ul>
        <li><a href="/api/status">/api/status</a> - Estado del servidor</li>
        <li><a href="/api/sensors">/api/sensors</a> - Datos de sensores IoT</li>
        <li><a href="/api/weather">/api/weather</a> - Datos del clima</li>
        <li><a href="/api/all">/api/all</a> - Todos los datos</li>
        <li><a href="/api/heatmap">/api/heatmap</a> - Datos para mapa de calor</li>
        <li><a href="/api/all-data">/api/all-data</a> - Historial completo</li>
    </ul>
    """

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Iniciando CampusConnect Backend")
    print("=" * 50)
    print(f"📡 Servidor corriendo en: http://localhost:5000")
    print(f"🌍 OpenWeather API: {'✅ Configurada' if OPENWEATHER_API_KEY != 'TU_API_KEY_AQUI' else '❌ Sin configurar'}")
    print(f"🔧 Modo: {'Hardware Real' if 'readTemperatureHumidity' in dir() else 'Simulación'}")
    print("=" * 50)
    print("\nEndpoints disponibles:")
    print("  - http://localhost:5000/api/sensors")
    print("  - http://localhost:5000/api/weather")
    print("  - http://localhost:5000/api/all")
    print("  - http://localhost:5000/api/heatmap")
    print("\n💡 Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)