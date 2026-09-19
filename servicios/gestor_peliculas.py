import json
from modelos.pelicula import Pelicula
from estructuras.arbol_binario import ArbolBST
import bisect

class GestorPeliculas:
    def __init__(self):
        self._peliculas = []
        self._arbol_anio = ArbolBST()

    def cargar_desde_json(self, ruta = "datos/peliculas.json"):
        """Carga las películas desde el archivo JSON"""
        try:
            with open(ruta, "r", encoding = "utf-8") as archivos:
                datos = json.load(archivos)
                self._peliculas = [Pelicula(d["id"], d["titulo"], d["director"], d["genero"], d["rating"], d["anio"]) for d in datos]
                [self._arbol_anio.insertar(p, clave = lambda e: e.anio) for p in self._peliculas]
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo")
            self._peliculas = []
            self._arbol_anio = ArbolBST()

    def ordenar_por_anio(self):
        self._peliculas.sort(key = lambda p: p.anio)

    def buscar_binaria(self, anio: int):
        claves = [p.anio for p in self._peliculas]
        indice = bisect.bisect_left(claves, anio)
        if indice < len(claves) and claves[indice] == anio:
            return self._peliculas[indice]
        return None

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

    def buscar_por_anio(self, anio):
        """Busca películas según el año ingresado utilizando un árbol binario"""
        return self._arbol_anio.buscar(anio, clave = lambda e: e.anio)
    
    def buscar_por_anio_sec(self, anio):
        """Busca películas según el año ingresado utilizando búsqueda secuencial"""
        return [pel for pel in self._peliculas if anio == pel.anio]
