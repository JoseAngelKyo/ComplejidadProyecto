from fastapi import APIRouter
from supabase_client import supabase
import networkx as nx

router = APIRouter()

DESCRIPCION_ZONA = {
    "Lima Norte": "Zona de expansión urbana con alta conectividad residencial e industrial.",
    "Lima Centro": "Zona con mayor densidad de intersecciones y flujo vehicular intenso.",
    "Lima Sur": "Zona residencial-comercial con flujo medio de tráfico."
}


def construir_subgrafo(zonas: list):

    # =========================
    # NODOS
    # =========================

    nodos = supabase.table("intersecciones") \
        .select("*") \
        .in_("zona", zonas) \
        .execute().data

    nombres_validos = [n["nombre"] for n in nodos]

    # =========================
    # ARISTAS
    # =========================

    conexiones = supabase.table("conexiones") \
        .select("*") \
        .execute().data

    conexiones_filtradas = []

    for c in conexiones:

        if c["origen"] in nombres_validos and c["destino"] in nombres_validos:
            conexiones_filtradas.append(c)

    # =========================
    # GRAFO
    # =========================

    G = nx.Graph()

    for n in nodos:

        G.add_node(
            n["nombre"],
            **n
        )

    for c in conexiones_filtradas:

        G.add_edge(
            c["origen"],
            c["destino"],
            weight=float(c["distancia_km"])
        )

    grados = dict(G.degree())

    nodo_central = None

    if grados:
        nodo_central = max(grados, key=grados.get)

    return {
        "descripcion": [DESCRIPCION_ZONA[z] for z in zonas],
        "nodo_mas_conectado": nodo_central,
        "total_nodos": G.number_of_nodes(),
        "total_aristas": G.number_of_edges(),

        # ESTO ES LO IMPORTANTE PARA EL FRONT
        "nodos": nodos,
        "conexiones": conexiones_filtradas
    }


@router.get("/subgrafo")
def get_subgrafo(zona: str):

    zonas_validas = {

        "norte": ["Lima Norte"],
        "centro": ["Lima Centro"],
        "sur": ["Lima Sur"],
        "todas": [
            "Lima Norte",
            "Lima Centro",
            "Lima Sur"
        ]
    }

    zona = zona.lower()

    if zona not in zonas_validas:

        return {
            "error": "Zona inválida"
        }

    return construir_subgrafo(
        zonas_validas[zona]
    )
