import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

CARPETA_DATASET = "DataSet"
CARPETA_SUBGRAFOS = "DataSet_Subgrafo"

os.makedirs(CARPETA_SUBGRAFOS, exist_ok=True)

df_nodos = pd.read_csv(os.path.join(
    CARPETA_DATASET, "intersecciones_viales.csv"))
df_edges = pd.read_csv(os.path.join(
    CARPETA_DATASET, "conexiones_viales_trafico.csv"))

print("\n===================================")
print("        ANALISIS DE SUBGRAFOS      ")
print("===================================")

print("Selecciona una zona:")
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
    "Lima Norte": "Zona de alta expansión urbana con conectividad industrial y residencial.",
    "Lima Centro": "Núcleo principal de la ciudad con alta densidad de tráfico e intersecciones.",
    "Lima Sur": "Zona residencial y comercial con flujo medio de movilidad urbana."
}

print("\n===================================")
print("DESCRIPCIÓN DEL SUBGRAFO")
print("===================================")

for zona in zonas_seleccionadas:
    print(f"- {zona}: {descripcion_zona.get(zona, 'Zona urbana de análisis')}")

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

plt.title(f"Subgrafo Vial - {', '.join(zonas_seleccionadas)}", fontsize=14)
plt.axis("off")

plt.show()

archivo_salida = os.path.join(
    CARPETA_SUBGRAFOS,
    "subgrafo_seleccionado.csv"
)

df_sub = pd.DataFrame(list(G.edges()), columns=["origen", "destino"])
df_sub.to_csv(archivo_salida, index=False)

print("\n✔ Subgrafo guardado en:")
print(archivo_salida)
