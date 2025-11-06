# CampusConnect – Smart Social Spaces (IoT Challenge 2025-26)

**Team Members:**  
- Génesis Balcazar Escobar  
- Hugo Rey Insausti  

---

## Project Summary
CampusConnect is an IoT prototype designed to foster social cohesion and wellbeing on campus.  
By monitoring shared spaces through environmental and presence sensors, the system provides feedback
that promotes respectful behavior, collaborative use of resources, and informed decision-making about
where to socialize or study.

A public dashboard — the **“Campus Pulse”** — displays real-time status of multiple campus zones based
on noise, occupancy, and air quality levels. Visual feedback (LEDs or screen indicators) encourages
positive social interactions and responsible use of campus spaces.

---

## MVP Scope
During this course, we aim to develop a functional MVP with:

- Monitoring of **2 shared spaces** (e.g., study room + cafeteria area)
- **3 sensors per space**: noise level, presence/occupancy, and air quality/temperature
- Microcontroller nodes (ESP32 or Raspberry Pi) with Wi-Fi communication (MQTT)
- Cloud/local backend with storage (InfluxDB or SQLite)
- Real-time dashboard using Grafana or ThingsBoard
- Local visual feedback through a LED strip or small display

---

## Repository Structure
/hardware → Wiring diagrams, photos, build references
/firmware → Microcontroller code (ESP32/Arduino)
/backend → Scripts and services for MQTT, data storage, APIs
/dashboard → Grafana/ThingsBoard dashboards, captures, exports
/docs → Written report (PDF), slides, references
/tests → Logs, test results, experiments



---

## Setup Overview
1. Flash firmware from `/firmware/` to the ESP32 nodes.
2. Deploy MQTT broker (Mosquitto recommended).
3. Run backend listener to store data into a database.
4. Load `/dashboard/` assets into Grafana or ThingsBoard.
5. Validate sensor → cloud → dashboard → visual feedback pipeline.

Detailed setup instructions will be added as the implementation progresses.
