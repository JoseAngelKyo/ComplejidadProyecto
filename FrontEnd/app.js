const API = "http://127.0.0.1:8000";

// =========================
// ESTADO GLOBAL
// =========================

let interseccionesGlobal = [];
let conexionesGlobal = [];

// =========================
// CARGAR INTERSECCIONES
// =========================

async function cargarIntersecciones() {
    const res = await fetch(`${API}/intersecciones`);
    interseccionesGlobal = await res.json();

    document.getElementById("totalIntersecciones").innerText =
        interseccionesGlobal.length;

    if (typeof llenarSelects === "function") {
        llenarSelects(interseccionesGlobal);
    }

    if (typeof pintarMapa === "function") {
        pintarMapa(interseccionesGlobal);
    }
}

// =========================
// CARGAR CONEXIONES
// =========================

async function cargarConexiones() {
    const res = await fetch(`${API}/conexiones`);
    conexionesGlobal = await res.json();

    document.getElementById("totalConexiones").innerText =
        conexionesGlobal.length;
}

// =========================
// INFO GRAFO
// =========================

async function cargarInfoGrafo() {
    const res = await fetch(`${API}/grafo/info`);
    const data = await res.json();

    console.log("INFO GRAFO:", data);
}

// =========================
// INICIO
// =========================

async function initApp() {
    await cargarIntersecciones();
    await cargarConexiones();
    await cargarInfoGrafo();
}

initApp();