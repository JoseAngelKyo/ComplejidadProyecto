from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import supabase
import networkx as nx

app = FastAPI(title="Sistema de Tráfico Inteligente - Lima")

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# CONSTRUIR GRAFO DESDE SUPABASE
# -----------------------------


def construir_grafo():
    response = supabase.table("conexiones").select("*").execute()
    conexiones = response.data

    G = nx.Graph()

    for c in conexiones:
        origen = c["origen"]
        destino = c["destino"]

        # peso principal = distancia
        distancia = float(c["distancia_km"])

        G.add_edge(origen, destino, weight=distancia, **c)

    return G


# -----------------------------
# INTERSECCIONES
# -----------------------------
@app.get("/intersecciones")
def get_intersecciones():
    response = supabase.table("intersecciones").select("*").execute()
    return response.data


# -----------------------------
# CONEXIONES
# -----------------------------
@app.get("/conexiones")
def get_conexiones():
    response = supabase.table("conexiones").select("*").execute()
    return response.data


# -----------------------------
# INFO DEL GRAFO
# -----------------------------
@app.get("/grafo/info")
def grafo_info():
    G = construir_grafo()
    return {
        "nodos": G.number_of_nodes(),
        "aristas": G.number_of_edges()
    }


# -----------------------------
# BFS (OBLIGATORIO)
# -----------------------------
@app.get("/bfs/{inicio}")
def bfs(inicio: str):
    G = construir_grafo()

    if inicio not in G:
        return {"error": "Nodo no existe"}

    recorrido = list(nx.bfs_tree(G, source=inicio))

    return {
        "inicio": inicio,
        "recorrido": recorrido
    }


# -----------------------------
# DIJKSTRA (OBLIGATORIO)
# -----------------------------
@app.get("/dijkstra")
def dijkstra(origen: str, destino: str):
    G = construir_grafo()

    if origen not in G or destino not in G:
        return {"error": "Nodo no existe"}

    try:
        camino = nx.shortest_path(
            G,
            source=origen,
            target=destino,
            weight="weight"
        )

        distancia_total = nx.shortest_path_length(
            G,
            source=origen,
            target=destino,
            weight="weight"
        )

        return {
            "origen": origen,
            "destino": destino,
            "camino": camino,
            "distancia_total": distancia_total
        }

    except nx.NetworkXNoPath:
        return {"error": "No existe ruta entre nodos"}


# -----------------------------
# KRUSKAL (MST - OBLIGATORIO)
# -----------------------------
@app.get("/kruskal")
def kruskal():
    G = construir_grafo()

    mst = nx.minimum_spanning_tree(G, weight="weight")

    return {
        "aristas_mst": list(mst.edges(data=True)),
        "costo_total": sum(d["weight"] for _, _, d in mst.edges(data=True))
    }
