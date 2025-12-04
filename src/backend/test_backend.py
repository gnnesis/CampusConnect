import requests
import time

API_URL = "http://localhost:5000"

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
    }
]

print("🧪 Probando backend...")

for data in test_data:
    response = requests.post(f'{API_URL}/api/sensor-data', json=data)
    if response.status_code == 200:
        print(f"✅ {data['sensor_id']}: OK")
    else:
        print(f"❌ {data['sensor_id']}: Error")

time.sleep(2)

print("\n📊 Verificando datos guardados...")
response = requests.get(f'{API_URL}/api/all-data')
print(f"Total registros: {len(response.json())}")