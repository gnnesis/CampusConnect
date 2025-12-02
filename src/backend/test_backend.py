import requests
import time

# Datos de prueba simulando sensores
test_data = [
    {
        'sensor_id': 'test_cafeteria',
        'latitude': 43.2711,
        'longitude': -2.9380,
        'intensity': 0.8,
        'category': 'social'
    },
    {
        'sensor_id': 'test_biblioteca',
        'latitude': 43.2708,
        'longitude': -2.9382,
        'intensity': 0.5,
        'category': 'study'
    },
    {
        'sensor_id': 'test_jardin',
        'latitude': 43.2714,
        'longitude': -2.9378,
        'intensity': 0.3,
        'category': 'relax'
    }
]

print("🧪 Enviando datos de prueba al backend...")

for data in test_data:
    try:
        response = requests.post('http://localhost:5000/api/sensor-data', json=data)
        if response.status_code == 200:
            print(f"✅ {data['sensor_id']}: OK")
        else:
            print(f"❌ {data['sensor_id']}: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n📊 Verificando datos guardados...")
try:
    response = requests.get('http://localhost:5000/api/all-data')
    data = response.json()
    print(f"✅ {len(data)} registros en la base de datos")
    for item in data[:3]:  # Mostrar los 3 primeros
        print(f"  - {item['sensor_id']}: {item['intensity']}")
except Exception as e:
    print(f"❌ Error: {e}")