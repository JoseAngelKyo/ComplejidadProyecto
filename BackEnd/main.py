from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import supabase
from subgrafo import router as subgrafo_router
import networkx as nx

app = FastAPI(title="Sistema de Tráfico Inteligente - Lima")

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# CONSTRUIR GRAFO DESDE SUPABASE
# ==========================================


def construir_grafo():

    response = supabase.table("conexiones").select("*").execute()

    conexiones = response.data

    G = nx.Graph()

    for c in conexiones:

        G.add_edge(
            c["origen"],
            c["destino"],
            weight=float(c["distancia_km"]),
            **c
        )

    return G

# ==========================================
# RUTA PRINCIPAL
# ==========================================


@app.get("/")
def inicio():

    return {
        "mensaje": "API Sistema de Tráfico Inteligente",
        "estado": "Funcionando correctamente"
    }

# ==========================================
# INTERSECCIONES
# ==========================================


@app.get("/intersecciones")
def obtener_intersecciones():

    return supabase.table("intersecciones").select("*").execute().data

# ==========================================
# CONEXIONES
# ==========================================


@app.get("/conexiones")
def obtener_conexiones():

    return supabase.table("conexiones").select("*").execute().data

# ==========================================
# INFORMACIÓN DEL GRAFO
# ==========================================


@app.get("/grafo/info")
def info_grafo():

    G = construir_grafo()

    return {
        "nodos": G.number_of_nodes(),
        "aristas": G.number_of_edges()
    }

# ==========================================
# BFS
# ==========================================


@app.get("/bfs/{inicio}")
def bfs(inicio: str):

    G = construir_grafo()

    if inicio not in G:

        return {"error": "Nodo no encontrado"}

    recorrido = list(nx.bfs_tree(G, inicio))

    return {
        "inicio": inicio,
        "recorrido": recorrido
    }

# ==========================================
# DIJKSTRA
# ==========================================


@app.get("/dijkstra")
def dijkstra(origen: str, destino: str):

    G = construir_grafo()

    if origen not in G or destino not in G:

        return {"error": "Nodo no encontrado"}

    try:

        camino = nx.shortest_path(
            G,
            source=origen,
            target=destino,
            weight="weight"
        )

        distancia = nx.shortest_path_length(
            G,
            source=origen,
            target=destino,
            weight="weight"
        )

        return {
            "origen": origen,
            "destino": destino,
            "camino": camino,
            "distancia_total": distancia
        }

    except nx.NetworkXNoPath:

        return {
            "error": "No existe un camino entre esos nodos"
        }

# ==========================================
# KRUSKAL (ÁRBOL DE EXPANSIÓN MÍNIMA)
# ==========================================


@app.get("/kruskal")
def kruskal():

    G = construir_grafo()

    mst = nx.minimum_spanning_tree(
        G,
        weight="weight"
    )

    return {

        "numero_aristas": mst.number_of_edges(),

        "costo_total": sum(
            datos["weight"]
            for _, _, datos in mst.edges(data=True)
        ),

        "aristas": list(
            mst.edges(data=True)
        )
    }


# -----------------------------
# 🔥 SUBGRAFO (DIVIDE Y VENCERÁS)
# -----------------------------
app.include_router(subgrafo_router)
