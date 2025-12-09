// Inicializar el mapa centrado en Universidad de Deusto
const map = L.map('map').setView([43.271123311528505, -2.9380385763615475], 18);

// Añadir capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 21,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Datos de ejemplo simulando sensores IoT
// Formato: [latitud, longitud, intensidad (0-1)]
const dataPoints = {
    all: [
        // Cafetería principal
        [43.2711, -2.9380, 0.9],
        [43.2712, -2.9381, 0.85],
        [43.2710, -2.9379, 0.8],
        
        // Biblioteca
        [43.2708, -2.9382, 0.7],
        [43.2709, -2.9383, 0.75],
        
        // Zona de descanso exterior
        [43.2714, -2.9378, 0.6],
        [43.2715, -2.9377, 0.65],
        
        // Aulas principales
        [43.2707, -2.9380, 0.5],
        [43.2706, -2.9381, 0.55]
    ],
    
    social: [
        // Cafetería (alta interacción)
        [43.2711, -2.9380, 1.0],
        [43.2712, -2.9381, 0.95],
        [43.2710, -2.9379, 0.9],
        
        // Zona común
        [43.2713, -2.9379, 0.8],
        [43.2714, -2.9378, 0.75]
    ],
    
    relax: [
        // Jardín/zona verde
        [43.2714, -2.9378, 0.85],
        [43.2715, -2.9377, 0.9],
        [43.2716, -2.9376, 0.8],
        
        // Sala de descanso
        [43.2709, -2.9377, 0.7]
    ],
    
    food: [
        // Cafetería
        [43.2711, -2.9380, 1.0],
        [43.2712, -2.9381, 0.95],
        [43.2710, -2.9379, 0.9],
        
        // Máquinas vending
        [43.2708, -2.9379, 0.6]
    ],
    
    study: [
        // Biblioteca
        [43.2708, -2.9382, 0.9],
        [43.2709, -2.9383, 0.85],
        [43.2707, -2.9383, 0.8],
        
        // Salas de estudio
        [43.2707, -2.9380, 0.75],
        [43.2706, -2.9381, 0.7]
    ]
};

// Variable para almacenar la capa de calor actual
let currentHeatLayer = null;

// Función para crear y mostrar el mapa de calor
function showHeatmap(category) {
    // Remover capa anterior si existe
    if (currentHeatLayer) {
        map.removeLayer(currentHeatLayer);
    }
    
    // Crear nueva capa de calor
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
    
    // Actualizar estadísticas
    updateStats(category);
}

// Función para actualizar el panel de estadísticas
function updateStats(category, points) {
    const stats = document.getElementById('stats');
    const categoryNames = {
        all: 'Todas las áreas',
        social: 'Zonas de interacción social',
        relax: 'Áreas de relajación',
        food: 'Puntos de comida',
        study: 'Espacios de estudio'
    };
    
    // Si no hay puntos, usar datos de ejemplo
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

// Añadir marcadores con información
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

// Event listeners para los botones de filtro
document.querySelectorAll('.filter-btn').forEach(button => {
    button.addEventListener('click', function() {
        // Quitar clase active de todos los botones
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Añadir clase active al botón clickeado
        this.classList.add('active');
        
        // Mostrar el mapa de calor correspondiente
        const filter = this.getAttribute('data-filter');
        showHeatmap(filter);
    });
});

// Simular actualización de datos en tiempo real
function simulateRealTimeData() {
    setInterval(() => {
        const activeFilter = document.querySelector('.filter-btn.active').getAttribute('data-filter');
        
        // Añadir pequeñas variaciones a los datos
        dataPoints[activeFilter] = dataPoints[activeFilter].map(point => {
            const variation = (Math.random() - 0.5) * 0.1;
            return [point[0], point[1], Math.max(0.1, Math.min(1.0, point[2] + variation))];
        });
        
        // Actualizar el mapa
        showHeatmap(activeFilter);
    }, 5000); // Actualizar cada 5 segundos
}

// Inicializar la aplicación
showHeatmap('all');
addMarkers();
simulateRealTimeData();