from supabase_client import supabase
import random
import os

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

TIPOS_INTERSECCION = ["cruce", "rotonda", "interseccion principal"]
TIPOS_VIA = ["calle", "avenida", "autopista"]
PRIORIDADES = ["baja", "media", "alta"]

intersecciones_generadas = []

print("Generando intersecciones...")

for i in range(1, NUM_INTERSECCIONES + 1):

    distrito = random.choice(DISTRITOS)
    nombre = f"{distrito}_{i}"
    zona = ZONAS[distrito]

    latitud = round(random.uniform(-12.25, -11.85), 6)
    longitud = round(random.uniform(-77.20, -76.85), 6)

    tipo_interseccion = random.choice(TIPOS_INTERSECCION)
    semaforo = random.choice(["si", "no"])

    supabase.table("intersecciones").insert({
        "id_interseccion": i,
        "nombre": nombre,
        "distrito": distrito,
        "zona": zona,
        "latitud": latitud,
        "longitud": longitud,
        "tipo_interseccion": tipo_interseccion,
        "semaforo": semaforo
    }).execute()

    intersecciones_generadas.append({
        "nombre": nombre,
        "distrito": distrito
    })

print(f"Intersecciones generadas: {NUM_INTERSECCIONES}")

print("Generando conexiones...")

for _ in range(NUM_CONEXIONES):

    origen = random.choice(intersecciones_generadas)
    distrito_origen = origen["distrito"]

    distritos_validos = DISTRITOS_CERCANOS[distrito_origen]

    posibles_destinos = [
        x for x in intersecciones_generadas
        if x["distrito"] in distritos_validos
    ]

    destino = random.choice(posibles_destinos)

    while destino["nombre"] == origen["nombre"]:
        destino = random.choice(posibles_destinos)

    tipo_via = random.choice(TIPOS_VIA)

    if tipo_via == "calle":
        distancia = random.randint(1, 5)
        velocidad = random.choice([30, 40])
        nivel_trafico = random.choice([2, 3, 4])

    elif tipo_via == "avenida":
        distancia = random.randint(3, 10)
        velocidad = random.choice([50, 60])
        nivel_trafico = random.choice([1, 2, 3])

    else:
        distancia = random.randint(8, 15)
        velocidad = random.choice([80, 100])
        nivel_trafico = random.choice([1, 2])

    trafico = (
        "trafico libre" if nivel_trafico == 1 else
        "trafico moderado" if nivel_trafico == 2 else
        "trafico alto" if nivel_trafico == 3 else
        "trafico extremo"
    )

    tiempo = random.randint(distancia * 2, distancia * 5)

    supabase.table("conexiones").insert({
        "origen": origen["nombre"],
        "destino": destino["nombre"],
        "tipo_via": tipo_via,
        "distancia_km": distancia,
        "tiempo_min": tiempo,
        "nivel_trafico": nivel_trafico,
        "trafico": trafico,
        "capacidad": random.choice([40, 60, 100, 150, 250, 500]),
        "velocidad_max": velocidad,
        "prioridad_via": random.choice(PRIORIDADES),
        "bidireccional": random.choice(["si", "no"])
    }).execute()

print("Conexiones generadas:", NUM_CONEXIONES)

print("\n=========================================")
print("SIMULACION URBANA COMPLETADA EN SUPABASE")
print("=========================================")
