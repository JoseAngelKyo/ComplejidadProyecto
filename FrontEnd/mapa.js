const API = "http://127.0.0.1:8000";

// =========================
// MAPA
// =========================
const map = L.map("mapa").setView([-12.05, -77.05], 12);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "Lima Smart System"
}).addTo(map);

// =========================
// ESTADO GLOBAL
// =========================
let nodos = [];
let conexiones = [];
let markers = [];
let lines = [];

// =========================
// NORMALIZAR TEXTO (CLAVE FIX)
// =========================
function norm(t) {
    return (t || "").trim().toLowerCase();
}

// =========================
// BUSCAR NODO (FIX DEFINITIVO)
// =========================
function getNodo(nombre) {
    return nodos.find(n => norm(n.nombre) === norm(nombre));
}

// =========================
// LIMPIAR LINEAS
// =========================
function limpiarLineas() {
    lines.forEach(l => map.removeLayer(l));
    lines = [];
}

// =========================
// CARGAR NODOS
// =========================
async function cargarNodos() {

    const res = await fetch(`${API}/intersecciones`);
    nodos = await res.json();

    document.getElementById("intersecciones").innerText = nodos.length;

    // markers
    nodos.forEach(n => {
        const m = L.circleMarker([n.latitud, n.longitud], {
            radius: 6,
            color: "#38bdf8",
            fillColor: "#38bdf8",
            fillOpacity: 0.8
        }).addTo(map);

        markers.push(m);
    });

    llenarSelects();
}

// =========================
// CARGAR CONEXIONES
// =========================
async function cargarConexiones() {

    const res = await fetch(`${API}/conexiones`);
    conexiones = await res.json();

    dibujarGrafoBase();
}

// =========================
// GRAFO BASE
// =========================
function dibujarGrafoBase() {

    limpiarLineas();

    conexiones.forEach(c => {

        const a = getNodo(c.origen);
        const b = getNodo(c.destino);

        if (!a || !b) return;

        const line = L.polyline([
            [a.latitud, a.longitud],
            [b.latitud, b.longitud]
        ], {
            color: "#334155",
            weight: 2,
            opacity: 0.5
        }).addTo(map);

        lines.push(line);
    });
}

// =========================
// DIBUJAR RUTA
// =========================
function dibujarRuta(lista, color) {

    limpiarLineas();

    for (let i = 0; i < lista.length - 1; i++) {

        const a = getNodo(lista[i]);
        const b = getNodo(lista[i + 1]);

        if (!a || !b) continue;

        const line = L.polyline([
            [a.latitud, a.longitud],
            [b.latitud, b.longitud]
        ], {
            color,
            weight: 5,
            opacity: 0.9
        }).addTo(map);

        lines.push(line);
    }
}

// =========================
// SELECTS
// =========================
function llenarSelects() {

    const o = document.getElementById("origen");
    const d = document.getElementById("destino");

    o.innerHTML = "";
    d.innerHTML = "";

    nodos.forEach(n => {
        o.innerHTML += `<option value="${n.nombre}">${n.nombre}</option>`;
        d.innerHTML += `<option value="${n.nombre}">${n.nombre}</option>`;
    });
}

// =========================
// BFS
// =========================
document.getElementById("btnBFS").addEventListener("click", async () => {

    const inicio = document.getElementById("origen").value;

    const res = await fetch(`${API}/bfs/${inicio}`);
    const data = await res.json();

    document.getElementById("algoritmo").innerText = "BFS";
    document.getElementById("intersecciones").innerText = data.recorrido.length;

    dibujarRuta(data.recorrido, "#3b82f6");
});

// =========================
// DIJKSTRA
// =========================
document.getElementById("btnDijkstra").addEventListener("click", async () => {

    const o = document.getElementById("origen").value;
    const d = document.getElementById("destino").value;

    const res = await fetch(`${API}/dijkstra?origen=${o}&destino=${d}`);
    const data = await res.json();

    document.getElementById("algoritmo").innerText = "Dijkstra";
    document.getElementById("distancia").innerText = data.distancia + " km";

    dibujarRuta(data.camino, "#10b981");
});

// =========================
// KRUSKAL
// =========================
document.getElementById("btnKruskal").addEventListener("click", async () => {

    const res = await fetch(`${API}/kruskal`);
    const data = await res.json();

    document.getElementById("algoritmo").innerText = "Kruskal";
    document.getElementById("distancia").innerText = data.costo_total + " km";
});

// =========================
// INIT SEGURO (CLAVE)
// =========================
async function init() {
    await cargarNodos();
    await cargarConexiones();
}

init();