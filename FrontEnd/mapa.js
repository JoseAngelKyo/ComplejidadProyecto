const API = "http://127.0.0.1:8000";

// =========================
// MAPA
// =========================

const map = L.map("mapa").setView([-12.05, -77.05], 12);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "Lima Smart System"
}).addTo(map);

// =========================
// VARIABLES
// =========================

let nodos = [];
let conexiones = [];
let markers = [];
let lines = [];

// =========================
// UTILIDADES
// =========================

function norm(t) {
    return (t || "").trim().toLowerCase();
}

function getNodo(nombre) {
    return nodos.find(n => norm(n.nombre) === norm(nombre));
}

function limpiarLineas() {
    lines.forEach(l => map.removeLayer(l));
    lines = [];
}

function limpiarMarkers() {
    markers.forEach(m => map.removeLayer(m));
    markers = [];
}

// =========================
// DIBUJAR NODOS
// =========================

function dibujarNodos() {

    limpiarMarkers();

    nodos.forEach(n => {

        const marker = L.circleMarker(
            [n.latitud, n.longitud],
            {
                radius: 6,
                color: "#38bdf8",
                fillColor: "#38bdf8",
                fillOpacity: 0.8,
                weight: 2
            }
        ).addTo(map);

        marker.bindPopup(`
            <b>${n.nombre}</b><br>
            Zona: ${n.zona}<br>
            Distrito: ${n.distrito}<br>
            Semáforo: ${n.semaforo}
        `);

        markers.push(marker);

    });

    if (markers.length > 0) {

        const grupo = L.featureGroup(markers);

        map.fitBounds(grupo.getBounds(), {
            padding: [40, 40]
        });

    }

}

// =========================
// DIBUJAR GRAFO
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
            opacity: 1
        }).addTo(map);

        lines.push(line);

    }

}

// =========================
// SELECTS
// =========================

function llenarSelects() {

    const origen = document.getElementById("origen");
    const destino = document.getElementById("destino");

    origen.innerHTML = "";
    destino.innerHTML = "";

    nodos.forEach(n => {

        origen.innerHTML += `<option value="${n.nombre}">${n.nombre}</option>`;
        destino.innerHTML += `<option value="${n.nombre}">${n.nombre}</option>`;

    });

}

// =========================
// CARGAR TODA LIMA
// =========================

async function cargarTodaLima() {

    const res1 = await fetch(`${API}/intersecciones`);
    nodos = await res1.json();

    const res2 = await fetch(`${API}/conexiones`);
    conexiones = await res2.json();

    dibujarNodos();
    dibujarGrafoBase();
    llenarSelects();

}

// =========================
// DIVIDE Y VENCERÁS
// =========================

async function cargarSubgrafo() {

    const zona = document.getElementById("zona").value;

    let parametro = "todas";

    if (zona === "Lima Norte") parametro = "norte";
    if (zona === "Lima Centro") parametro = "centro";
    if (zona === "Lima Sur") parametro = "sur";

    const res = await fetch(`${API}/subgrafo?zona=${parametro}`);
    const data = await res.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    nodos = data.nodos;
    conexiones = data.conexiones;

    // Limpiar mapa
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    limpiarLineas();

    // Dibujar nodos
    nodos.forEach(n => {

        const marker = L.circleMarker(
            [n.latitud, n.longitud],
            {
                radius: 6,
                color: "#38bdf8",
                fillColor: "#38bdf8",
                fillOpacity: 0.8
            }
        ).addTo(map);

        marker.bindPopup(`
            <b>${n.nombre}</b><br>
            ${n.distrito}<br>
            ${n.zona}
        `);

        markers.push(marker);

    });

    // Dibujar conexiones
    dibujarGrafoBase();

    // Actualizar selects
    llenarSelects();

    // ===========================
    // AJUSTAR VISTA POR ZONA
    // ===========================

    if (parametro === "norte") {

        map.setView([-11.93, -77.05], 12);

    } else if (parametro === "centro") {

        map.setView([-12.05, -77.04], 13);

    } else if (parametro === "sur") {

        map.setView([-12.18, -76.98], 12);

    } else {

        const grupo = L.featureGroup(markers);

        map.fitBounds(grupo.getBounds(), {
            padding: [40, 40]
        });

    }

    console.log(data.descripcion);

}
document.getElementById("zona").addEventListener("change", cargarSubgrafo);

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

    const origen = document.getElementById("origen").value;
    const destino = document.getElementById("destino").value;

    const res = await fetch(`${API}/dijkstra?origen=${origen}&destino=${destino}`);

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
// INICIO
// =========================

cargarTodaLima();