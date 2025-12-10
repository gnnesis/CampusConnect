// ========================
// CONFIGURACIÓN
// ========================
const API_URL = "http://localhost:5000"; // URL del backend

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
const SENSOR_API_URL = "http://localhost:5001/api/sensors"; // tu backend de Flask

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

        // También puedes actualizar stats si quieres
        const stats = document.getElementById('stats');
        stats.innerHTML = `
            <p><strong>Categoría:</strong> ${data.category}</p>
            <p><strong>Puntos activos:</strong> 1 sensor</p>
            <p><strong>Intensidad promedio:</strong> --%</p>
            <p><strong>Última actualización:</strong> ${new Date(data.timestamp).toLocaleTimeString('es-ES')}</p>
        `;
    } catch (err) {
        console.error("Error obteniendo datos de sensores:", err);
    }
}

// Actualizar cada 10 segundos (coincide con el auto-save del backend)
fetchSensorData(); // fetch inicial
setInterval(fetchSensorData, 10000);

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
        gradient: {
            0.0: 'blue',
            0.3: 'cyan',
            0.5: 'lime',
            0.7: 'yellow',
            1.0: 'red'
        }
    }).addTo(map);

    updateStats(category);
}

function updateStats(category, points) {
    const stats = document.getElementById('stats');
    const categoryNames = {
        all: 'Todas las áreas',
        social: 'Zonas de interacción social',
        relax: 'Áreas de relajación',
        food: 'Puntos de comida',
        study: 'Espacios de estudio'
    };

    if (!points || points.length === 0) {
        points = dataPoints[category];
    }

    const avgIntensity = (points.reduce((sum, p) => sum + p[2], 0) / points.length * 100).toFixed(1);

    stats.innerHTML = `
        <p><strong>Categoría:</strong> ${categoryNames[category]}</p>
        <p><strong>Puntos de datos:</strong> ${points.length} sensores activos</p>
        <p><strong>Intensidad promedio:</strong> ${avgIntensity}%</p>
        <p><strong>Última actualización:</strong> ${new Date().toLocaleTimeString('es-ES')}</p>
    `;
}

function addMarkers() {
    const markers = [
        { pos: [43.2711, -2.9380], name: '☕ Cafetería Principal', desc: 'Alto tráfico de estudiantes' },
        { pos: [43.2708, -2.9382], name: '📚 Biblioteca', desc: 'Zona de estudio tranquila' },
        { pos: [43.2714, -2.9378], name: '🌳 Zona Verde', desc: 'Área de descanso al aire libre' }
    ];

    markers.forEach(marker => {
        L.marker(marker.pos)
            .addTo(map)
            .bindPopup(`<strong>${marker.name}</strong><br>${marker.desc}`);
    });
}

// ========================
// FILTROS DE BOTONES
// ========================
document.querySelectorAll('.filter-btn').forEach(button => {
    button.addEventListener('click', function() {
        document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        const filter = this.getAttribute('data-filter');
        showHeatmap(filter);
    });
});

// ========================
// SIMULACIÓN DE DATOS EN TIEMPO REAL
// ========================
function simulateRealTimeData() {
    setInterval(() => {
        const activeFilter = document.querySelector('.filter-btn.active').getAttribute('data-filter');
        dataPoints[activeFilter] = dataPoints[activeFilter].map(point => {
            const variation = (Math.random() - 0.5) * 0.1;
            return [point[0], point[1], Math.max(0.1, Math.min(1.0, point[2] + variation))];
        });
        showHeatmap(activeFilter);
    }, 5000);
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

        const iconEl = document.getElementById("weather-icon-main");
        const main = data.weather_main.toLowerCase();
        const icons = {
            clear: "☀️",
            clouds: "☁️",
            rain: "🌧️",
            drizzle: "🌦️",
            thunderstorm: "⛈️",
            snow: "❄️",
            mist: "🌫️",
            haze: "🌫️",
            fog: "🌫️"
        };
        iconEl.textContent = icons[main] || "☁️";

    } catch (err) {
        console.error("Error obteniendo clima:", err);
    }
}

// ========================
// INICIALIZACIÓN
// ========================
showHeatmap('all');
addMarkers();
simulateRealTimeData();
fetchWeather();
setInterval(fetchWeather, 10000); // actualizar clima cada 10s
