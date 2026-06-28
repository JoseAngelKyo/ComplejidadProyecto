"""Generación y análisis de subgrafos por zonas urbanas de Lima"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os


CARPETA_DATASET = "DataSet"

df_nodos = pd.read_csv(os.path.join(
    CARPETA_DATASET, "intersecciones_viales.csv"))

df_edges = pd.read_csv(os.path.join(
    CARPETA_DATASET, "conexiones_viales_trafico.csv"))

print("\n===================================")
print("        ANALISIS DE SUBGRAFOS      ")
print("===================================")

print("1. Lima Norte")
print("2. Lima Centro")
print("3. Lima Sur")
print("4. Todas")
opcion = input("\nOpción: ")

zonas_map = {
    "1": ["Lima Norte"],
    "2": ["Lima Centro"],
    "3": ["Lima Sur"],
    "4": ["Lima Norte", "Lima Centro", "Lima Sur"]
}

zonas_seleccionadas = zonas_map.get(opcion, ["Lima Centro"])

descripcion_zona = {
    "Lima Norte": "Zona de expansión urbana con alta conectividad residencial e industrial.",
    "Lima Centro": "Zona con mayor densidad de intersecciones y flujo vehicular intenso.",
    "Lima Sur": "Zona residencial-comercial con flujo medio de tráfico."
}

print("\n===================================")
print("DESCRIPCIÓN DEL SUBGRAFO")
print("===================================")

for zona in zonas_seleccionadas:
    print(f"- {zona}: {descripcion_zona[zona]}")

df_nodos_filtrados = df_nodos[df_nodos["zona"].isin(zonas_seleccionadas)]
nodos_validos = df_nodos_filtrados["nombre"].tolist()

df_edges_filtrados = df_edges[
    df_edges["origen"].isin(nodos_validos) &
    df_edges["destino"].isin(nodos_validos)
]

G = nx.from_pandas_edgelist(
    df_edges_filtrados,
    source="origen",
    target="destino",
    create_using=nx.Graph()
)

print("\n===================================")
print("ANÁLISIS DEL SUBGRAFO")
print("===================================")

print(f"Nodos: {G.number_of_nodes()}")
print(f"Aristas: {G.number_of_edges()}")

if len(G.nodes) > 0:
    grados = dict(G.degree())
    nodo_central = max(grados, key=grados.get)
    print(
        f"Nodo más conectado: {nodo_central} ({grados[nodo_central]} conexiones)")

plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)

nx.draw_networkx_nodes(G, pos, node_size=30, node_color="skyblue")
nx.draw_networkx_edges(G, pos, alpha=0.4)

plt.title(f"Subgrafo Vial - {', '.join(zonas_seleccionadas)}")
plt.axis("off")
plt.show()
