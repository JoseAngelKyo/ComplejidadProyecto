from subgrafo import router as subgrafo_router
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import supabase
import networkx as nx

app = FastAPI(title="Sistema de Tráfico Inteligente - Lima")


@app.get("/intersecciones")
def intersecciones():
    data = supabase.table("intersecciones").select("*").execute().data
    return data


@app.get("/conexiones")
def conexiones():
    data = supabase.table("conexiones").select("*").execute().data
    return data


@app.get("/")
def home():
    return {
        "mensaje": "API de Tráfico Lima activa",
        "estado": "OK"
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def construir_grafo():
    data = supabase.table("conexiones").select("*").execute().data
    G = nx.Graph()

    for c in data:
        G.add_edge(
            c["origen"],
            c["destino"],
            weight=float(c["distancia_km"])
        )

    return G


bfs_router = APIRouter()


@bfs_router.get("/bfs/{inicio}")
def bfs(inicio: str):
    G = construir_grafo()

    if inicio not in G:
        return {"error": "Nodo no encontrado"}

    recorrido = list(nx.bfs_tree(G, inicio))

    return {"inicio": inicio, "recorrido": recorrido}


dijkstra_router = APIRouter()


@dijkstra_router.get("/dijkstra")
def dijkstra(origen: str, destino: str):
    G = construir_grafo()

    try:
        camino = nx.shortest_path(G, origen, destino, weight="weight")
        distancia = nx.shortest_path_length(
            G, origen, destino, weight="weight")

        return {
            "origen": origen,
            "destino": destino,
            "camino": camino,
            "distancia": distancia
        }

    except:
        return {"error": "No hay ruta"}


kruskal_router = APIRouter()


@kruskal_router.get("/kruskal")
def kruskal():
    G = construir_grafo()
    mst = nx.minimum_spanning_tree(G, weight="weight")

    return {
        "aristas": list(mst.edges(data=True)),
        "costo_total": sum(d["weight"] for _, _, d in mst.edges(data=True))
    }


@app.get("/fuerza/{inicio}/{fin}")
def fuerza_bruta(inicio: str, fin: str):
    G = construir_grafo()

    rutas = list(nx.all_simple_paths(G, inicio, fin, cutoff=5))

    if not rutas:
        return {"error": "No hay rutas"}

    mejor = min(rutas, key=len)

    return {
        "total": len(rutas),
        "mejor": mejor
    }


@app.get("/maxflow")
def maxflow(origen: str, destino: str):
    G = construir_grafo().to_directed()

    for u, v in G.edges():
        G[u][v]["capacity"] = 10

    flujo, _ = nx.maximum_flow(G, origen, destino)

    return {"flujo_maximo": flujo}


@app.get("/scc")
def scc():
    G = construir_grafo().to_directed()
    componentes = list(nx.strongly_connected_components(G))

    return {
        "componentes": [list(c) for c in componentes]
    }


@app.get("/ufds")
def ufds():
    data = supabase.table("conexiones").select("*").execute().data

    parent = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        parent[find(a)] = find(b)

    nodos = set()

    for c in data:
        nodos.add(c["origen"])
        nodos.add(c["destino"])

    for n in nodos:
        parent[n] = n

    for c in data:
        union(c["origen"], c["destino"])

    grupos = {}
    for n in nodos:
        r = find(n)
        grupos.setdefault(r, []).append(n)

    return {"grupos": list(grupos.values())}


@app.get("/dp")
def dp(origen: str, destino: str):
    G = construir_grafo()

    memo = {}

    def f(n):
        if n == destino:
            return 0
        if n in memo:
            return memo[n]

        mejor = float("inf")

        for v in G[n]:
            mejor = min(mejor, G[n][v]["weight"] + f(v))

        memo[n] = mejor
        return mejor

    return {"costo_minimo": f(origen)}


app.include_router(bfs_router)
app.include_router(dijkstra_router)
app.include_router(kruskal_router)
app.include_router(subgrafo_router)
