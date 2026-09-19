import json
import random

generos = ["Ciencia Ficción", "Acción", "Comedia", "Drama"]
directores = ["Nolan", "Wachowski", "Fincher", "Tarantino"]

def generar(n: int) -> None:
    peliculas = [
        {
            "id": random.randint(1, n),
            "titulo": f"Pelicula {i}",
            "director": random.choice(directores),
            "genero": random.choice(generos),
            "rating": round(random.uniform(1.0, 10.0), 1),
            "anio": random.randint(1910, 2026),
        }
        for i in range(n)
    ]
    ruta = f"datos/peliculas_{n}.json"
    with open(ruta, "w", encoding = "utf-8") as archivo:
        json.dump(peliculas, archivo, ensure_ascii = False, indent = 2)
    print(ruta)

for n in (100, 1000, 10000, 100000):
    generar(n)