from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Base de datos en la misma carpeta
DB_PATH = 'sensor_data.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            latitude REAL,
            longitude REAL,
            intensity REAL,
            category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Base de datos inicializada")

init_db()

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    try:
        data = request.json
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO sensor_readings 
            (sensor_id, latitude, longitude, intensity, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['sensor_id'],
            data['latitude'],
            data['longitude'],
            data['intensity'],
            data['category']
        ))
        conn.commit()
        conn.close()
        
        print(f"Datos recibidos: {data['sensor_id']} = {data['intensity']:.2f}")
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/heatmap-data/<category>', methods=['GET'])
def get_heatmap_data(category):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if category == 'all':
            c.execute('''
                SELECT latitude, longitude, AVG(intensity) as avg_intensity
                FROM sensor_readings
                WHERE timestamp > datetime('now', '-5 minutes')
                GROUP BY sensor_id
            ''')
        else:
            c.execute('''
                SELECT latitude, longitude, AVG(intensity) as avg_intensity
                FROM sensor_readings
                WHERE category = ? 
                AND timestamp > datetime('now', '-5 minutes')
                GROUP BY sensor_id
            ''', (category,))
        
        rows = c.fetchall()
        conn.close()
        
        data = [[row[0], row[1], row[2]] for row in rows]
        
        print(f"Enviando {len(data)} puntos para '{category}'")
        return jsonify(data)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify([]), 500

@app.route('/api/all-data', methods=['GET'])
def get_all_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 50')
    rows = c.fetchall()
    conn.close()
    
    data = [{
        'id': row[0],
        'sensor_id': row[1],
        'latitude': row[2],
        'longitude': row[3],
        'intensity': row[4],
        'category': row[5],
        'timestamp': row[6]
    } for row in rows]
    
    return jsonify(data)

if __name__ == '__main__':
    print("Servidor iniciado en http://localhost:5000")
    print("Esperando datos de sensores...")
    app.run(host='0.0.0.0', port=5000, debug=True)

