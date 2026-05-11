"""Generación del dataset sintético de intersecciones y conexiones viales urbanas simuladas"""

import csv
import random
import os

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

DISTRITOS_CERCANOS = {
    "Miraflores": ["Barranco", "San Isidro", "Surco"],
    "San Isidro": ["Miraflores", "San Borja", "Rimac"],
    "Barranco": ["Miraflores", "Chorrillos", "Surco"],
    "Surco": ["Barranco", "San Borja", "La Molina"],
    "La Molina": ["Surco", "Ate", "San Borja"],
    "Ate": ["La Molina", "San Juan de Lurigancho"],
    "San Borja": ["San Isidro", "Surco", "La Molina"],
    "Chorrillos": ["Barranco", "Villa El Salvador"],
    "Comas": ["Los Olivos", "Rimac"],
    "Los Olivos": ["Comas", "Callao"],
    "San Miguel": ["Callao", "San Isidro"],
    "Callao": ["San Miguel", "Los Olivos"],
    "Villa El Salvador": ["Chorrillos", "Surco"],
    "Rimac": ["Comas", "San Isidro"],
    "San Juan de Lurigancho": ["Ate", "Rimac"]
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

PRIORIDADES = [
    "baja",
    "media",
    "alta"
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

        latitud = round(random.uniform(-12.25, -11.85), 6)

        longitud = round(random.uniform(-77.20, -76.85), 6)

        tipo_interseccion = random.choice(TIPOS_INTERSECCION)

        semaforo = random.choice(["si", "no"])

        writer.writerow([
            i,
            nombre,
            distrito,
            zona,
            latitud,
            longitud,
            tipo_interseccion,
            semaforo
        ])

        intersecciones_generadas.append({
            "nombre": nombre,
            "distrito": distrito
        })

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

        origen_data = random.choice(intersecciones_generadas)

        distrito_origen = origen_data["distrito"]

        distritos_validos = DISTRITOS_CERCANOS[distrito_origen]

        posibles_destinos = [
            x for x in intersecciones_generadas
            if x["distrito"] in distritos_validos
        ]

        destino_data = random.choice(posibles_destinos)

        while destino_data["nombre"] == origen_data["nombre"]:
            destino_data = random.choice(posibles_destinos)

        origen = origen_data["nombre"]

        destino = destino_data["nombre"]

        tipo_via = random.choice(TIPOS_VIA)

        if tipo_via == "calle":
            distancia = random.randint(1, 5)
            velocidad = random.choice(["30 km/h", "40 km/h"])
            trafico = random.choice([
                "trafico moderado",
                "trafico alto",
                "trafico extremo"
            ])

        elif tipo_via == "avenida":
            distancia = random.randint(3, 10)
            velocidad = random.choice(["50 km/h", "60 km/h"])
            trafico = random.choice([
                "trafico libre",
                "trafico moderado",
                "trafico alto"
            ])

        else:
            distancia = random.randint(8, 15)
            velocidad = random.choice(["80 km/h", "100 km/h"])
            trafico = random.choice([
                "trafico libre",
                "trafico moderado"
            ])

        tiempo = random.randint(
            distancia * 2,
            distancia * 5
        )

        capacidad = random.choice([
            "40 vehiculos",
            "60 vehiculos",
            "100 vehiculos",
            "150 vehiculos",
            "250 vehiculos",
            "500 vehiculos"
        ])

        prioridad = random.choice(PRIORIDADES)

        bidireccional = random.choice(["si", "no"])

        writer.writerow([
            origen,
            destino,
            tipo_via,
            f"{distancia} km",
            f"{tiempo} min",
            trafico,
            capacidad,
            velocidad,
            prioridad,
            bidireccional
        ])

print("\n=========================================")
print("SIMULACION URBANA GENERADA")
print("=========================================")

print(f"\nIntersecciones creadas: {NUM_INTERSECCIONES}")
print(f"Conexiones creadas: {NUM_CONEXIONES}")

print("\nArchivos generados correctamente.")
print(f"\n{RUTA_INTERSECCIONES}")
print(f"{RUTA_CONEXIONES}")

print("\n=========================================")
