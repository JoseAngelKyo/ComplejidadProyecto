from fastapi import APIRouter
from supabase_client import supabase
import networkx as nx

router = APIRouter()

# -----------------------------
# DESCRIPCIÓN DE ZONAS
# -----------------------------
DESCRIPCION_ZONA = {
    "Lima Norte": "Zona de expansión urbana con alta conectividad residencial e industrial.",
    "Lima Centro": "Zona con mayor densidad de intersecciones y flujo vehicular intenso.",
    "Lima Sur": "Zona residencial-comercial con flujo medio de tráfico."
}

# -----------------------------
# CONSTRUIR SUBGRAFO DESDE SUPABASE
# -----------------------------


def construir_subgrafo(zonas: list):
    nodos = supabase.table("intersecciones").select(
        "*").in_("zona", zonas).execute().data

    nombres_validos = [n["nombre"] for n in nodos]

    edges = supabase.table("conexiones").select("*").execute().data

    edges_filtrados = [
        e for e in edges
        if e["origen"] in nombres_validos and e["destino"] in nombres_validos
    ]

    G = nx.Graph()

    for n in nodos:
        G.add_node(n["nombre"], **n)

    for e in edges_filtrados:
        G.add_edge(e["origen"], e["destino"],
                   weight=float(e["distancia_km"]), **e)

    return G


# -----------------------------
# API: SUBGRAFO POR ZONA
# -----------------------------
@router.get("/subgrafo")
def get_subgrafo(zona: str):
    zonas_validas = {
        "norte": ["Lima Norte"],
        "centro": ["Lima Centro"],
        "sur": ["Lima Sur"],
        "todas": ["Lima Norte", "Lima Centro", "Lima Sur"]
    }

    zonas = zonas_validas.get(zona.lower())

    if not zonas:
        return {"error": "Zona inválida. Usa: norte, centro, sur, todas"}

    G = construir_subgrafo(zonas)

    grados = dict(G.degree())
    nodo_central = None

    if grados:
        nodo_central = max(grados, key=grados.get)

    return {
        "zonas": zonas,
        "nodos": G.number_of_nodes(),
        "aristas": G.number_of_edges(),
        "nodo_mas_conectado": nodo_central,
        "descripcion": [DESCRIPCION_ZONA[z] for z in zonas]
    }
