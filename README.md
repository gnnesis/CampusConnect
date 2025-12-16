# CampusConnect – Smart Social Spaces  
**IoT Challenge 2025–26**

---

## Team Members
- Génesis Balcazar Escobar  
- Hugo Rey Insausti  

---

## Project Overview
CampusConnect is an IoT prototype designed to improve social wellbeing and responsible use of shared campus spaces.  
The system monitors environmental and occupancy conditions in real time and provides feedback through a public dashboard called **Campus Pulse** and local visual indicators.

---

## Project Objectives
- Help students find quiet or available study spaces  
- Encourage respectful behavior in shared areas  
- Improve comfort and wellbeing on campus  
- Provide data for campus space management  

---

## What the System Does
- Measures noise level, presence/occupancy, and air quality  
- Sends sensor data using MQTT  
- Stores data in InfluxDB  
- Displays real-time data in Grafana dashboards  
- Provides local visual feedback using an LED strip  

---

## Sensors Used
| Sensor | Purpose |
|------|--------|
| Noise sensor (microphone) | Measure ambient sound level |
| Presence sensor (PIR / ToF) | Detect occupancy |
| Air quality / temperature sensor (MQ-135 / DHT22 / BME680) | Measure air quality, temperature, and humidity |
| LED strip | Provide visual feedback |

---

## Hardware Connections (ESP32 Example)
- **Microphone:** Analog input (GPIO 34 / 35 / 36)  
- **PIR sensor:** Digital input (GPIO 14 / 27)  
- **Air quality sensor:** I2C (SDA → GPIO 21, SCL → GPIO 22)  
- **LED strip:** Digital output (GPIO 5)  

**Power Supply:**
- 3.3V for most sensors  
- 5V for LED strip and some air quality sensors  

---

## System Workflow
1. Sensors collect environmental and occupancy data  
2. ESP32 processes the data and publishes it via MQTT  
3. Backend receives MQTT messages and stores data in InfluxDB  
4. Grafana reads the database and updates dashboards  
5. LED strip shows local feedback  
6. Users consult the Campus Pulse dashboard  

---

## Repository Structure

- `/hardware`  
  - Wiring diagrams and photos

- `/firmware`  
  - ESP32 firmware  
  - `main.cpp` → Main application logic  
  - `config.h` → Wi-Fi, MQTT and pin configuration  
  - `/sensors` → Sensor drivers

- `/backend`  
  - MQTT listener  
  - InfluxDB writer scripts

- `/dashboard`  
  - Grafana dashboards (JSON files)

- `/docs`  
  - Reports and presentation slides

---

## How to Run the Project

### 1. Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
2. Start InfluxDB (Docker)
bash
Copiar código
docker run -d \
  --name influxdb2 \
  -p 8086:8086 \
  -v influxdb-data:/var/lib/influxdb2 \
  influxdb:2
Default configuration:

User: admin

Password: admin123

Bucket: sensors

3. Start Grafana
bash
Copiar código
cd dashboard
docker compose up -d
Grafana credentials:

User: admin

Password: admin123

4. Flash ESP32 Firmware
Open the /firmware folder in Arduino IDE or PlatformIO

Update Wi-Fi and MQTT settings in config.h

Upload the firmware to the ESP32

5. Run Backend Listener
bash
Copiar código
cd backend
source ../venv/bin/activate
python mqtt_listener.py
6. Load Grafana Dashboard
Open Grafana in your browser

Import the dashboard JSON from /dashboard

Select InfluxDB as the data source

The dashboard updates in real time.

Project Status
This project is a functional IoT prototype that integrates sensors, data processing, and real-time visualization to improve shared campus spaces.
