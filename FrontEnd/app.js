const API = "http://127.0.0.1:8000";

async function cargarIntersecciones() {
    const res = await fetch(`${API}/intersecciones`);
    const data = await res.json();

    document.getElementById("output").innerText =
        JSON.stringify(data.slice(0, 10), null, 2);
}

async function cargarConexiones() {
    const res = await fetch(`${API}/conexiones`);
    const data = await res.json();

    document.getElementById("output").innerText =
        JSON.stringify(data.slice(0, 10), null, 2);
}

async function verGrafo() {
    const res = await fetch(`${API}/grafo/info`);
    const data = await res.json();

    document.getElementById("output").innerText =
        JSON.stringify(data, null, 2);
}