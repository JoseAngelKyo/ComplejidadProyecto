import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# =========================================================
# CARPETAS
# =========================================================

CARPETA_DATASET = "DataSet"
CARPETA_SUBGRAFOS = "DataSet_Subgrafo"

os.makedirs(CARPETA_SUBGRAFOS, exist_ok=True)

# =========================================================
# CARGAR DATASET
# =========================================================

df_nodos = pd.read_csv(os.path.join(CARPETA_DATASET, "intersecciones_viales.csv"))
df_edges = pd.read_csv(os.path.join(CARPETA_DATASET, "conexiones_viales_trafico.csv"))

# =========================================================
# SELECCIÓN DE ZONA
# =========================================================

print("\n===================================")
print("SELECCIONA UNA ZONA")
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

# =========================================================
# FILTRAR NODOS Y CONEXIONES
# =========================================================

df_nodos_filtrados = df_nodos[df_nodos["zona"].isin(zonas_seleccionadas)]
nodos_validos = df_nodos_filtrados["nombre"].tolist()

df_edges_filtrados = df_edges[
    df_edges["origen"].isin(nodos_validos) &
    df_edges["destino"].isin(nodos_validos)
]

# =========================================================
# CREAR GRAFO
# =========================================================

G = nx.from_pandas_edgelist(
    df_edges_filtrados,
    source="origen",
    target="destino",
    create_using=nx.Graph()
)

# =========================================================
# ANÁLISIS
# =========================================================

print("\n===================================")
print("ANÁLISIS DEL SUBGRAFO")
print("===================================")

print(f"Nodos: {G.number_of_nodes()}")
print(f"Aristas: {G.number_of_edges()}")

if len(G.nodes) > 0:
    grados = dict(G.degree())
    nodo_central = max(grados, key=grados.get)
    print(f"Nodo más conectado: {nodo_central} ({grados[nodo_central]} conexiones)")

# =========================================================
# VISUALIZACIÓN
# =========================================================

plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    node_size=20,
    with_labels=False
)

plt.title(f"Subgrafo - {', '.join(zonas_seleccionadas)}")
plt.show()

# =========================================================
# EXPORTAR SUBGRAFO
# =========================================================

archivo_salida = os.path.join(
    CARPETA_SUBGRAFOS,
    "subgrafo_seleccionado.csv"
)

df_sub = pd.DataFrame(list(G.edges()), columns=["origen", "destino"])
df_sub.to_csv(archivo_salida, index=False)

print("\n✔ Subgrafo guardado en:")
print(archivo_salida)