const API = "http://127.0.0.1:8000";

let interseccionesGlobal = [];
let conexionesGlobal = [];

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

async function cargarConexiones() {
    const res = await fetch(`${API}/conexiones`);
    conexionesGlobal = await res.json();

    document.getElementById("totalConexiones").innerText =
        conexionesGlobal.length;
}

async function cargarInfoGrafo() {
    const res = await fetch(`${API}/grafo/info`);
    const data = await res.json();

    console.log("INFO GRAFO:", data);
}

async function initApp() {
    await cargarIntersecciones();
    await cargarConexiones();
    await cargarInfoGrafo();
}

initApp();