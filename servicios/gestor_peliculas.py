import json
from modelos.pelicula import Pelicula

class GestorPeliculas:
    def __init__(self):
        self._peliculas = []

    def cargar_desde_json(self):
        """Carga las películas desde el archivo JSON"""
        try:
            with open("datos/peliculas.json", "r", encoding = "utf-8") as archivos:
                datos = json.load(archivos)
                self._peliculas = [Pelicula(d["id"], d["titulo"], d["director"], d["genero"], d["rating"], d["anio"]) for d in datos]
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo")
            self._peliculas = []

    def mostrar_peliculas(self):
        """Imprime por pantalla todas las películas ordenadas de forma numerada."""
        if not self._peliculas:
            print("No hay películas registradas en el catálogo.")
            return

        for i, pelicula in enumerate(self._peliculas, 1):
            print(f"{i}. {pelicula}")

    def buscar_por_titulo(self, titulo):
        """Busca películas según el título ingresado"""
        titulo_lower = titulo.lower().strip()
        return [pel for pel in self._peliculas if titulo_lower in pel.titulo.lower()]

    def buscar_por_director(self, director):
        """Busca películas según el director ingresado"""
        director_lower = director.lower().strip()
        return [pel for pel in self._peliculas if director_lower in pel.director.lower()]
    
    def buscar_por_genero(self, genero):
        """Busca películas según el género ingresado"""
        genero_lower = genero.lower().strip()
        return [pel for pel in self._peliculas if genero_lower in pel.genero.lower()]

    def obtener_top_n_mejores(self, n):
        """Devuelve las N películas con mayor rating"""
        peliculas_ordenadas = sorted(self._peliculas, key = lambda p: p.rating, reverse = True)
        return peliculas_ordenadas[:n]

    def obtener_relacionadas(self, pelicula):
        """Devuelve películas relacionadas que compartan el mismo género, excluyendo la película utilizada de referencia"""
        return [p for p in self._peliculas if p.genero.lower() == pelicula.genero.lower() and p.titulo.lower() != pelicula.titulo.lower()]