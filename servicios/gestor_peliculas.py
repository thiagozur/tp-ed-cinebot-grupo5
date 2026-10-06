import json
from modelos.pelicula import Pelicula
from estructuras.arbol_binario import ArbolBST
from estructuras.avl import AVL
from estructuras.arbol_general import ArbolGeneral
import bisect

class GestorPeliculas:
    def __init__(self):
        self._peliculas = []
        self._arbol_anio = ArbolBST()
        self._avl_titulo = AVL()
        self._bst_director = ArbolBST()
        self._bst_genero = ArbolBST()
        self.generos = {}
        self._arbol_categorias = ArbolGeneral()

    def cargar_desde_json(self, ruta = "datos/peliculas.json"):
        """Carga las películas desde el archivo JSON"""
        try:
            with open(ruta, "r", encoding = "utf-8") as archivos:
                datos = json.load(archivos)
                self._peliculas = [Pelicula(d["id"], d["titulo"], d["director"], d["genero"], d["rating"], d["anio"]) for d in datos]
                raiz_categorias = self._arbol_categorias.insertar_raiz("Categorías")
                for p in self._peliculas:
                    self._arbol_anio.insertar(p, clave = lambda e: e.anio)
                    self._avl_titulo.insertar(p, clave = lambda e: e.titulo)
                    self._bst_director.insertar(p, clave = lambda e: e.director)
                    self._bst_genero.insertar(p, clave = lambda e: e.genero)
                    genero = p.genero
                    if genero not in self.generos:
                        nodo_g = self._arbol_categorias.agregar_hijo(raiz_categorias, genero)
                        self.generos[genero] = nodo_g
                    self._arbol_categorias.agregar_hijo(self.generos[genero], p)
                    
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo")
            self._peliculas = []
            self._arbol_anio = ArbolBST()
            self._avl_titulo = AVL()
            self._bst_director = ArbolBST()
            self._bst_genero = ArbolBST()
            self._arbol_categorias = ArbolGeneral()

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
        """Busca películas según el título ingresado (utilizando un AVL)"""
        titulo_lower = titulo.lower().strip()
        return [self._avl_titulo.buscar(titulo_lower, lambda e: e.titulo.lower())] if self._avl_titulo.buscar(titulo_lower, lambda e: e.titulo.lower()) else []

    def buscar_por_director(self, director):
        """Busca películas según el director ingresado (utilizando un BST)"""
        director_lower = director.lower().strip()
        return self._bst_director.buscar(director_lower, lambda e: e.director.lower())
    
    def buscar_por_genero(self, genero):
        """Busca películas según el género ingresado (utilizando un BST)"""
        genero_lower = genero.lower().strip()
        return self._bst_genero.buscar(genero_lower, lambda e: e.genero.lower())

    def obtener_top_n_mejores(self, n):
        """Devuelve las N películas con mayor rating"""
        peliculas_ordenadas = sorted(self._peliculas, key = lambda p: p.rating, reverse = True)
        return peliculas_ordenadas[:n]

    def obtener_relacionadas(self, pelicula):
        """Devuelve películas relacionadas que compartan el mismo género, excluyendo la película utilizada de referencia"""
        return [p for p in self._peliculas if p.genero.lower() == pelicula.genero.lower() and p.titulo.lower() != pelicula.titulo.lower()]

    def buscar_por_anio(self, anio):
        """Busca películas según el año ingresado (utilizando un BST)"""
        return self._arbol_anio.buscar(anio, clave = lambda e: e.anio)
    
    def buscar_por_anio_sec(self, anio):
        """Busca películas según el año ingresado utilizando búsqueda secuencial"""
        return [pel for pel in self._peliculas if anio == pel.anio]

    def mostrar_categorias(self, nodo = None, nivel = 0, solo_cat = True):
        """Imprime por pantalla las categorías guardadas en el árbol general. Si solo_cat es False, también se muestran las películas"""
        if nodo is None:
            if self._arbol_categorias.raiz is None:
                print("Árbol vacío")
                return
            nodo = self._arbol_categorias.raiz

        prefijo = " " * nivel + "└─" if nivel > 0 else ""
        str_dato = nodo.dato.titulo if hasattr(nodo.dato, "titulo") else str(nodo.dato).capitalize()

        print(f"{prefijo}{str_dato}")

        if solo_cat:
            if nivel >= 1:
                return
            
        for hijo in nodo.hijos:
            self.mostrar_categorias(hijo, nivel + 1, solo_cat)