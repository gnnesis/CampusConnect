from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

app = Flask(__name__)
CORS(app)

# ============================================
# ⭐ CONFIGURACIÓN INFLUXDB
# ============================================
INFLUX_URL = "http://10.172.117.140:8087"
INFLUX_TOKEN = "vrAK4VDblEmBWNreJJF2oY65lGGaJcuKTVxWui087dDGEYH7zVV64QXlNjEKA0mILZ4_yOxHlUh2op4G9lgNVA==" 
INFLUX_ORG = "Deusto"
INFLUX_BUCKET = "deusto"

# Cliente InfluxDB
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

print("✅ Conectado a InfluxDB")

# ============================================
# ENDPOINT 1: Recibir datos de sensores
# ============================================
@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    try:
        data = request.json
        
        # Crear punto de datos
        point = Point("sensor_reading") \
            .tag("sensor_id", data['sensor_id']) \
            .tag("category", data['category']) \
            .field("latitude", float(data['latitude'])) \
            .field("longitude", float(data['longitude'])) \
            .field("intensity", float(data['intensity']))
        
        # Escribir en InfluxDB
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        
        print(f"📊 {data['sensor_id']}: {data['intensity']:.2f}")
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============================================
# ENDPOINT 2: Datos para el mapa de calor
# ============================================
@app.route('/api/heatmap-data/<category>', methods=['GET'])
def get_heatmap_data(category):
    try:
        if category == 'all':
            query = f'''
                from(bucket: "{INFLUX_BUCKET}")
                |> range(start: -5m)
                |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
                |> filter(fn: (r) => r["_field"] == "intensity" or r["_field"] == "latitude" or r["_field"] == "longitude")
                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
                |> group(columns: ["sensor_id"])
                |> mean()
            '''
        else:
            query = f'''
                from(bucket: "{INFLUX_BUCKET}")
                |> range(start: -5m)
                |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
                |> filter(fn: (r) => r["category"] == "{category}")
                |> filter(fn: (r) => r["_field"] == "intensity" or r["_field"] == "latitude" or r["_field"] == "longitude")
                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
                |> group(columns: ["sensor_id"])
                |> mean()
            '''
        
        result = query_api.query(org=INFLUX_ORG, query=query)
        
        data = []
        for table in result:
            for record in table.records:
                try:
                    lat = record.values.get('latitude')
                    lon = record.values.get('longitude')
                    intensity = record.values.get('intensity')
                    
                    if lat and lon and intensity:
                        data.append([lat, lon, intensity])
                except:
                    continue
        
        print(f"📍 {len(data)} puntos para '{category}'")
        return jsonify(data)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify([]), 500

# ============================================
# ENDPOINT 3: Debug - ver todos los datos
# ============================================
@app.route('/api/all-data', methods=['GET'])
def get_all_data():
    try:
        query = f'''
            from(bucket: "{INFLUX_BUCKET}")
            |> range(start: -1h)
            |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
            |> limit(n: 50)
        '''
        
        result = query_api.query(org=INFLUX_ORG, query=query)
        
        data = []
        for table in result:
            for record in table.records:
                data.append({
                    'time': record.get_time().isoformat(),
                    'sensor_id': record.values.get('sensor_id'),
                    'category': record.values.get('category'),
                    'field': record.get_field(),
                    'value': record.get_value()
                })
        
        return jsonify(data)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify([]), 500

if __name__ == '__main__':
    print("🚀 Servidor Flask iniciado en puerto 5000")
    print("📡 Esperando datos de sensores...")
    app.run(host='0.0.0.0', port=5000, debug=True)