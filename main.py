import csv
import random
import os

# ==========================================
# CREAR CARPETA DATASET
# ==========================================

CARPETA_DATASET = "DataSet"

os.makedirs(CARPETA_DATASET, exist_ok=True)

# ==========================================
# CONFIGURACIÓN
# ==========================================

NUM_REGISTROS = 5000

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

# ==========================================
# RUTA DEL ARCHIVO CSV
# ==========================================

RUTA_ARCHIVO = os.path.join(
    CARPETA_DATASET,
    "trafico_vial_lima.csv"
)

# ==========================================
# GENERAR CSV
# ==========================================

with open(
    RUTA_ARCHIVO,
    mode="w",
    newline="",
    encoding="utf-8"
) as archivo:

    writer = csv.writer(
        archivo,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_ALL
    )

    # CABECERA
    writer.writerow([
        "origen",
        "destino",
        "zona_origen",
        "zona_destino",
        "tipo_via",
        "distancia_km",
        "tiempo_min",
        "trafico",
        "capacidad",
        "velocidad_max",
        "prioridad_via",
        "semaforo",
        "bidireccional"
    ])

    # GENERAR DATOS
    for _ in range(NUM_REGISTROS):

        origen = random.choice(DISTRITOS)

        destino = random.choice(DISTRITOS)

        while destino == origen:
            destino = random.choice(DISTRITOS)

        zona_origen = ZONAS[origen]

        zona_destino = ZONAS[destino]

        tipo_via = random.choice(TIPOS_VIA)

        distancia_km = f"{random.randint(1, 15)} km"

        tiempo_min = f"{random.randint(3, 60)} min"

        trafico = random.choice(TRAFICOS)

        capacidad = random.choice(CAPACIDADES)

        velocidad_max = random.choice(VELOCIDADES)

        prioridad_via = random.choice(PRIORIDADES)

        semaforo = random.randint(0, 1)

        bidireccional = random.randint(0, 1)

        writer.writerow([
            origen,
            destino,
            zona_origen,
            zona_destino,
            tipo_via,
            distancia_km,
            tiempo_min,
            trafico,
            capacidad,
            velocidad_max,
            prioridad_via,
            semaforo,
            bidireccional
        ])

print("\nDataset generado correctamente.")
print(f"Archivo creado en: {RUTA_ARCHIVO}")
