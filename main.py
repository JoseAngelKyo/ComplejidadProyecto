import csv
import random

# =========================================
# CONFIGURACIÓN GENERAL
# =========================================

NUM_NODOS = 1500
NUM_CALLES = 5000

ZONAS = ["Centro", "Norte", "Sur", "Este", "Oeste"]

TIPOS_NODO = [
    "interseccion",
    "rotonda",
    "cruce"
]

TIPOS_VIA = [
    "calle",
    "avenida",
    "autopista"
]

ESTADOS_VIA = [
    "libre",
    "congestionada",
    "cerrada"
]

PRIORIDADES = [
    "alta",
    "media",
    "baja"
]

# =========================================
# GENERAR nodos.csv
# =========================================

with open(
    "nodos.csv",
    mode="w",
    newline="",
    encoding="utf-8"
) as archivo_nodos:

    writer = csv.writer(
        archivo_nodos,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_ALL
    )

    # CABECERA
    writer.writerow([
        "id_nodo",
        "nombre",
        "zona",
        "tipo_nodo",
        "latitud",
        "longitud",
        "semaforo"
    ])

    # DATOS
    for i in range(1, NUM_NODOS + 1):

        id_nodo = f"N{i}"

        nombre = f"Interseccion_{i}"

        zona = random.choice(ZONAS)

        tipo_nodo = random.choice(TIPOS_NODO)

        latitud = round(random.uniform(-12.20, -11.90), 6)

        longitud = round(random.uniform(-77.20, -76.90), 6)

        semaforo = random.randint(0, 1)

        writer.writerow([
            id_nodo,
            nombre,
            zona,
            tipo_nodo,
            latitud,
            longitud,
            semaforo
        ])

# =========================================
# GENERAR calles.csv
# =========================================

with open(
    "calles.csv",
    mode="w",
    newline="",
    encoding="utf-8"
) as archivo_calles:

    writer = csv.writer(
        archivo_calles,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_ALL
    )

    # CABECERA
    writer.writerow([
        "id_calle",
        "origen",
        "destino",
        "distancia_km",
        "tiempo_min",
        "trafico",
        "capacidad_vehiculos",
        "flujo_actual",
        "velocidad_max_kmh",
        "tipo_via",
        "zona",
        "estado_via",
        "semaforo",
        "bidireccional",
        "prioridad"
    ])

    # DATOS
    for i in range(1, NUM_CALLES + 1):

        origen = f"N{random.randint(1, NUM_NODOS)}"

        destino = f"N{random.randint(1, NUM_NODOS)}"

        while destino == origen:
            destino = f"N{random.randint(1, NUM_NODOS)}"

        distancia_km = round(random.uniform(0.3, 10.0), 2)

        tiempo_min = round(
            distancia_km * random.uniform(2, 6),
            2
        )

        trafico = round(random.uniform(0.0, 1.0), 2)

        capacidad_vehiculos = random.randint(50, 500)

        flujo_actual = random.randint(
            0,
            capacidad_vehiculos
        )

        velocidad_max_kmh = random.choice([
            30,
            40,
            50,
            60,
            80,
            100
        ])

        tipo_via = random.choice(TIPOS_VIA)

        zona = random.choice(ZONAS)

        estado_via = random.choice(ESTADOS_VIA)

        semaforo = random.randint(0, 1)

        bidireccional = random.randint(0, 1)

        prioridad = random.choice(PRIORIDADES)

        writer.writerow([
            i,
            origen,
            destino,
            distancia_km,
            tiempo_min,
            trafico,
            capacidad_vehiculos,
            flujo_actual,
            velocidad_max_kmh,
            tipo_via,
            zona,
            estado_via,
            semaforo,
            bidireccional,
            prioridad
        ])

print("\nCSV generados correctamente.")
print("-> nodos.csv")
print("-> calles.csv")
