import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

import simulacion

df_intersecciones = pd.read_csv(
    "DataSet/intersecciones_viales.csv"
)

df_conexiones = pd.read_csv(
    "DataSet/conexiones_viales_trafico.csv"
)

G = nx.from_pandas_edgelist(
    df_conexiones,
    source="origen",
    target="destino",
    create_using=nx.Graph()
)

plt.figure(figsize=(14, 10))

pos = nx.spring_layout(
    G,
    seed=42,
    k=0.15
)

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=15
)

nx.draw_networkx_edges(
    G,
    pos,
    alpha=0.3
)

plt.title(
    "Red Vial Inteligente - Sistema de Trafico Urbano",
    fontsize=16
)

plt.axis("off")

plt.show()

print("\n=========================================")
print("ANALISIS DEL GRAFO")
print("=========================================")

print(f"\nCantidad total de nodos: {G.number_of_nodes()}")

print(f"Cantidad total de aristas: {G.number_of_edges()}")

print("\n=========================================")
print("Visualizacion completada correctamente.")
print("=========================================")
