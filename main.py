
import csv
import random
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


CARPETA_DATASET = "DataSet"
os.makedirs(CARPETA_DATASET, exist_ok=True)

NUM_INTERSECCIONES = 1500
NUM_CONEXIONES = 1500

DISTRITOS = [
    "Miraflores",
    "San Isidro",
    "Barranco",
    "Surco",
    "La Molina",
    "Ate",
    "San Borja",
    "Chorrillos",
    "Comas",
    "Los Olivos",
    "San Miguel",
    "Callao",
    "Villa El Salvador",
    "Rimac",
    "San Juan de Lurigancho"
]

ZONAS = {
    "Miraflores": "Lima Sur",
    "San Isidro": "Lima Centro",
    "Barranco": "Lima Sur",
    "Surco": "Lima Sur",
    "La Molina": "Lima Este",
    "Ate": "Lima Este",
    "San Borja": "Lima Centro",
    "Chorrillos": "Lima Sur",
    "Comas": "Lima Norte",
    "Los Olivos": "Lima Norte",
    "San Miguel": "Lima Oeste",
    "Callao": "Lima Oeste",
    "Villa El Salvador": "Lima Sur",
    "Rimac": "Lima Centro",
    "San Juan de Lurigancho": "Lima Este"
}

TIPOS_INTERSECCION = [
    "cruce",
    "rotonda",
    "interseccion principal"
]

TIPOS_VIA = [
    "calle",
    "avenida",
    "autopista"
]

TRAFICOS = [
    "trafico libre",
    "trafico moderado",
    "trafico alto",
    "trafico extremo"
]

PRIORIDADES = [
    "baja",
    "media",
    "alta"
]

VELOCIDADES = [
    "30 km/h",
    "40 km/h",
    "50 km/h",
    "60 km/h",
    "80 km/h",
    "100 km/h"
]

CAPACIDADES = [
    "40 vehiculos",
    "60 vehiculos",
    "100 vehiculos",
    "150 vehiculos",
    "250 vehiculos",
    "500 vehiculos"
]

RUTA_INTERSECCIONES = os.path.join(
    CARPETA_DATASET,
    "intersecciones_viales.csv"
)

RUTA_CONEXIONES = os.path.join(
    CARPETA_DATASET,
    "conexiones_viales_trafico.csv"
)

intersecciones_generadas = []

with open(
    RUTA_INTERSECCIONES,
    mode="w",
    newline="",
    encoding="utf-8"
) as archivo_intersecciones:

    writer = csv.writer(
        archivo_intersecciones,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_ALL
    )

    writer.writerow([
        "id_interseccion",
        "nombre",
        "zona",
        "latitud",
        "longitud",
        "tipo_interseccion",
        "semaforo"
    ])

    for i in range(1, NUM_INTERSECCIONES + 1):

        distrito = random.choice(DISTRITOS)

        nombre = f"{distrito}_{i}"

        zona = ZONAS[distrito]

        latitud = round(random.uniform(-12.25, -11.85), 6)

        longitud = round(random.uniform(-77.20, -76.85), 6)

        tipo_interseccion = random.choice(TIPOS_INTERSECCION)

        semaforo = random.randint(0, 1)

        writer.writerow([
            i,
            nombre,
            zona,
            latitud,
            longitud,
            tipo_interseccion,
            semaforo
        ])

        intersecciones_generadas.append(nombre)

with open(
    RUTA_CONEXIONES,
    mode="w",
    newline="",
    encoding="utf-8"
) as archivo_conexiones:

    writer = csv.writer(
        archivo_conexiones,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_ALL
    )

    writer.writerow([
        "origen",
        "destino",
        "tipo_via",
        "distancia_km",
        "tiempo_min",
        "trafico",
        "capacidad",
        "velocidad_max",
        "prioridad_via",
        "bidireccional"
    ])

    for _ in range(NUM_CONEXIONES):

        origen = random.choice(intersecciones_generadas)

        destino = random.choice(intersecciones_generadas)

        while destino == origen:
            destino = random.choice(intersecciones_generadas)

        tipo_via = random.choice(TIPOS_VIA)

        distancia_km = f"{random.randint(1, 15)} km"

        tiempo_min = f"{random.randint(3, 60)} min"

        trafico = random.choice(TRAFICOS)

        capacidad = random.choice(CAPACIDADES)

        velocidad_max = random.choice(VELOCIDADES)

        prioridad_via = random.choice(PRIORIDADES)

        bidireccional = random.randint(0, 1)

        writer.writerow([
            origen,
            destino,
            tipo_via,
            distancia_km,
            tiempo_min,
            trafico,
            capacidad,
            velocidad_max,
            prioridad_via,
            bidireccional
        ])

df_intersecciones = pd.read_csv(RUTA_INTERSECCIONES)

df_conexiones = pd.read_csv(RUTA_CONEXIONES)

G = nx.from_pandas_edgelist(
    df_conexiones,
    source="origen",
    target="destino",
    create_using=nx.Graph()
)

plt.figure(figsize=(12, 8))

pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    node_size=10,
    with_labels=False
)

plt.title("Red Vial Inteligente - Grafo de Intersecciones")
plt.show()

print("\n=========================================")
print("DATASET GENERADO CORRECTAMENTE")
print("=========================================")

print(f"\nIntersecciones creadas (Nodos): {NUM_INTERSECCIONES}")
print(f"Archivo generado: {RUTA_INTERSECCIONES}")

print(f"\nConexiones creadas (Aristas): {NUM_CONEXIONES}")
print(f"Archivo generado: {RUTA_CONEXIONES}")

print(f"\nCantidad total de nodos en el grafo: {G.number_of_nodes()}")
print(f"Cantidad total de aristas en el grafo: {G.number_of_edges()}")

print("\nUbicacion de los archivos:")
print(f"./{CARPETA_DATASET}/")

print("\n=========================================")
print("Proceso finalizado correctamente.")
print("=========================================")