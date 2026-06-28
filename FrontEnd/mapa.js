// =========================
// MAPA BASE LEAFLET
// =========================

const map = L.map('mapa').setView([-12.05, -77.05], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Lima Smart Urban System'
}).addTo(map);

// =========================
// VARIABLES GLOBALES
// =========================

let intersecciones = [];
let markers = [];

// Colores por zona
const colores = {
    "Lima Norte": "#3b82f6",
    "Lima Centro": "#10b981",
    "Lima Sur": "#f59e0b",
    "Lima Este": "#a855f7",
    "Lima Oeste": "#ef4444"
};

// =========================
// CARGAR DATOS DESDE BACKEND
// =========================

async function cargarIntersecciones() {

    const res = await fetch("http://127.0.0.1:8000/intersecciones");
    intersecciones = await res.json();

    document.getElementById("totalIntersecciones").innerText = intersecciones.length;

    pintarMapa();
    llenarSelects();
}

// =========================
// PINTAR MAPA
// =========================

function pintarMapa() {

    // limpiar markers anteriores
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    intersecciones.forEach(nodo => {

        const color = colores[nodo.zona] || "#64748b";

        const marker = L.circleMarker(
            [nodo.latitud, nodo.longitud],
            {
                radius: 6,
                color: color,
                fillColor: color,
                fillOpacity: 0.8,
                weight: 2
            }
        ).addTo(map);

        marker.bindPopup(`
            <b>${nodo.nombre}</b><br>
            Zona: ${nodo.zona}<br>
            Distrito: ${nodo.distrito}<br>
            Semáforo: ${nodo.semaforo}
        `);

        markers.push(marker);
    });
}

// =========================
// LLENAR SELECTS
// =========================

function llenarSelects() {

    const origen = document.getElementById("origen");
    const destino = document.getElementById("destino");

    origen.innerHTML = "";
    destino.innerHTML = "";

    intersecciones.forEach(nodo => {

        const option1 = document.createElement("option");
        option1.value = nodo.nombre;
        option1.textContent = nodo.nombre;

        const option2 = option1.cloneNode(true);

        origen.appendChild(option1);
        destino.appendChild(option2);
    });
}

// =========================
// BFS
// =========================

document.getElementById("btnBFS").addEventListener("click", async () => {

    const inicio = document.getElementById("origen").value;

    const res = await fetch(`http://127.0.0.1:8000/bfs/${inicio}`);
    const data = await res.json();

    document.getElementById("algoritmo").innerText = "BFS";
    document.getElementById("intersecciones").innerText = data.recorrido.length;
});

// =========================
// DIJKSTRA
// =========================

document.getElementById("btnDijkstra").addEventListener("click", async () => {

    const origen = document.getElementById("origen").value;
    const destino = document.getElementById("destino").value;

    const res = await fetch(`http://127.0.0.1:8000/dijkstra?origen=${origen}&destino=${destino}`);
    const data = await res.json();

    document.getElementById("algoritmo").innerText = "Dijkstra";
    document.getElementById("distancia").innerText = data.distancia_total + " km";
    document.getElementById("intersecciones").innerText = data.camino.length;
});

// =========================
// KRUSKAL
// =========================

document.getElementById("btnKruskal").addEventListener("click", async () => {

    const res = await fetch("http://127.0.0.1:8000/kruskal");
    const data = await res.json();

    document.getElementById("algoritmo").innerText = "Kruskal";
    document.getElementById("distancia").innerText = data.costo_total + " km";
});

// =========================
// INICIAR
// =========================

cargarIntersecciones();