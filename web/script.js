// ========================
// CONFIGURACIÓN
// ========================
const API_URL = "http://localhost:5001"; // URL del backend
let currentHeatLayer = null;

// Inicializamos puntos de ejemplo para heatmap
// Inicializamos puntos de ejemplo para heatmap (corregido)
const dataPoints = {
    all: [
        [43.2711, -2.9380, 0.5],
        [43.2708, -2.9382, 0.7],
        [43.2714, -2.9378, 0.3],
        [43.27133803087678, -2.9377551379742366, 0.5]  // este sería el cuarto pintxo
    ],
    social: [
        [43.2713679879075, -2.938815222975388, 0.6]
    ],
    relax: [
        [43.27075949744019, -2.937265027859081, 0.4],
        [43.27107288785087, -2.9363857869343892, 0.5]
    ],
    food: [
        [43.27108582275102, -2.936691133270228, 0.7]
    ],
    study: [
        [43.27133803087678, -2.9377551379742366, 0.5]
    ]
};



// ========================
// INICIALIZAR MAPA
// ========================
const map = L.map('map').setView([43.271123311528505, -2.9380385763615475], 18);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 21,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// ========================
// DATOS REALES DE SENSORES
// ========================
const SENSOR_API_URL = `${API_URL}/api/sensors`; // tu backend de Flask

async function fetchSensorData() {
    try {
        const res = await fetch(SENSOR_API_URL);
        const data = await res.json();

        // Actualizar DOM
        document.getElementById("temp-value").textContent = `${data.temperature.toFixed(1)}°C`;
        document.getElementById("humidity-value").textContent = `${data.humidity.toFixed(1)}%`;
        document.getElementById("noise-value").textContent = data.noise;
        document.getElementById("noise-status").textContent = data.noise_level;
        document.getElementById("air-value").textContent = data.air_quality;
        document.getElementById("air-status").textContent = data.air_status;
        document.getElementById("people-value").textContent = data.people_present ? "Sí" : "No";
        document.getElementById("distance-value").textContent = data.distance.toFixed(1);
        document.getElementById("sensor-update").textContent = `Última actualización: ${new Date(data.timestamp).toLocaleTimeString('es-ES')}`;

    } catch (err) {
        console.error("Error obteniendo datos de sensores:", err);
    }
}

// ========================
// FUNCIONES DE MAPA Y HEATMAP
// ========================
function showHeatmap(category) {
    if (currentHeatLayer) {
        map.removeLayer(currentHeatLayer);
    }

    currentHeatLayer = L.heatLayer(dataPoints[category], {
        radius: 25,
        blur: 35,
        maxZoom: 17,
        max: 1.0,
        gradient: {0.0: 'blue', 0.3: 'cyan', 0.5: 'lime', 0.7: 'yellow', 1.0: 'red'}
    }).addTo(map);
}

function addMarkers() {
    const markers = [
        { pos: [43.27177440959463, -2.9391453516571033], name: '☕ Cafetería Principal', desc: 'Alto tráfico de estudiantes' },
        { pos: [43.271380049714786, -2.937798139863879], name: '📚 Biblioteca', desc: 'Zona de estudio tranquila' },
        { pos: [43.271302716504934, -2.9388450675286926], name: '🌳 Zona Verde', desc: 'Área de descanso al aire libre' }
    ];

    markers.forEach(marker => {
        L.marker(marker.pos)
            .addTo(map)
            .bindPopup(`<strong>${marker.name}</strong><br>${marker.desc}`);
    });
}

// ========================
// FETCH DATOS CLIMA
// ========================
async function fetchWeather() {
    try {
        const res = await fetch(`${API_URL}/api/weather`);
        const data = await res.json();

        document.getElementById("current-temp").textContent = `${data.temperature.toFixed(1)}°`;
        document.getElementById("temp-max").textContent = `${data.temp_max.toFixed(1)}°`;
        document.getElementById("temp-min").textContent = `${data.temp_min.toFixed(1)}°`;
        document.getElementById("weather-desc-main").textContent = data.weather_desc;
        document.getElementById("rain-prob").textContent = `${data.rain_probability}%`;
        document.getElementById("humidity-ext").textContent = `${data.humidity}%`;
        document.getElementById("wind-speed").textContent = data.wind_speed;
        document.getElementById("feels-like").textContent = `${data.feels_like.toFixed(1)}°`;

    } catch (err) {
        console.error("Error obteniendo clima:", err);
    }
}

// ========================
// INICIALIZACIÓN
// ========================
document.addEventListener("DOMContentLoaded", () => {
    showHeatmap('all');
    addMarkers();
    fetchSensorData();
    fetchWeather();

    setInterval(fetchSensorData, 10000);
    setInterval(fetchWeather, 10000);
});
