import csv
import random
import os

# =========================================================
# CREAR CARPETA DATASET
# =========================================================

CARPETA_DATASET = "DataSet"
os.makedirs(CARPETA_DATASET, exist_ok=True)

RUTA_INTERSECCIONES = os.path.join(CARPETA_DATASET, "intersecciones_viales.csv")
RUTA_CONEXIONES = os.path.join(CARPETA_DATASET, "conexiones_viales_trafico.csv")

# =========================================================
# 🔒 EVITAR REGENERAR DATASET SI YA EXISTE
# =========================================================

if os.path.exists(RUTA_INTERSECCIONES) and os.path.exists(RUTA_CONEXIONES):
    print("Dataset ya existe. No se vuelve a generar.")
    exit()

# =========================================================
# CONFIGURACIÓN
# =========================================================

NUM_INTERSECCIONES = 1500
NUM_CONEXIONES = 1500

DISTRITOS = [
    "Miraflores", "San Isidro", "Barranco", "Surco", "La Molina",
    "Ate", "San Borja", "Chorrillos", "Comas", "Los Olivos",
    "San Miguel", "Callao", "Villa El Salvador", "Rimac",
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

TIPOS_INTERSECCION = ["cruce", "rotonda", "interseccion principal"]
TIPOS_VIA = ["calle", "avenida", "autopista"]

TRAFICOS = ["trafico libre", "trafico moderado", "trafico alto", "trafico extremo"]

CAPACIDADES = ["40 vehiculos", "60 vehiculos", "100 vehiculos", "150 vehiculos", "250 vehiculos"]

VELOCIDADES = ["30 km/h", "40 km/h", "50 km/h", "60 km/h", "80 km/h", "100 km/h"]

# =========================================================
# GENERAR INTERSECCIONES (NODOS)
# =========================================================

nodos = []

with open(RUTA_INTERSECCIONES, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "id_interseccion",
        "nombre",
        "distrito",
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

        lat = round(random.uniform(-12.25, -11.85), 6)
        lon = round(random.uniform(-77.20, -76.85), 6)

        tipo = random.choice(TIPOS_INTERSECCION)
        semaforo = random.randint(0, 1)

        nodos.append(nombre)

        writer.writerow([i, nombre, distrito, zona, lat, lon, tipo, semaforo])

# =========================================================
# GENERAR CONEXIONES (ARISTAS)
# =========================================================

with open(RUTA_CONEXIONES, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

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

        origen = random.choice(nodos)
        destino = random.choice(nodos)

        while origen == destino:
            destino = random.choice(nodos)

        writer.writerow([
            origen,
            destino,
            random.choice(TIPOS_VIA),
            random.randint(1, 15),
            random.randint(3, 60),
            random.choice(TRAFICOS),
            random.choice(CAPACIDADES),
            random.choice(VELOCIDADES),
            random.choice(["baja", "media", "alta"]),
            random.choice([0, 1])
        ])

# =========================================================
# MENSAJE FINAL
# =========================================================

print("\n=========================================")
print("DATASET GENERADO CORRECTAMENTE")
print("=========================================")

print(f"Nodos (intersecciones): {NUM_INTERSECCIONES}")
print(f"Aristas (conexiones): {NUM_CONEXIONES}")

print("\nArchivos guardados en:")
print("./DataSet/")