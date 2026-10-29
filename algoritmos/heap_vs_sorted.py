import time
import random
from estructuras.heaps import MaxHeap

def heap_vs_sorted(lista_datos):
    """Compara la implementación con sorted y con el montículo máximo de la funcionalidad de las top N películas.

    Retorna un diccionario con el tiempo en milisegundos que tarda cada implementación en encontrar la lista.
    """

    # MaxHeap generada al cargar el JSON de películas
    heap = MaxHeap()
    for d in lista_datos:
        heap.insertar((d.rating, d.titulo, d))

    # N top test
    valor_test = random.randrange(3, 15)

    # Búsqueda de los valores
    inicio = time.time()
    for _ in range(1000):
        top_n_heap = heap.obtener_top_n(valor_test)
    tiempo_heap = (time.time() - inicio) * 1000

    inicio = time.time()
    for _ in range(1000):
        peliculas_ordenadas = sorted(lista_datos, key = lambda p: p.rating, reverse = True)
        top_n_sorted = peliculas_ordenadas[:valor_test]
    tiempo_sorted = (time.time() - inicio) * 1000

    return {
        "tiempo_heap_ms": tiempo_heap,
        "tiempo_sorted_ms": tiempo_sorted,
    }

def main() -> None:
    import json
    from modelos.pelicula import Pelicula
    
    tamaños = (100, 1000, 10000, 100000)
    for n in tamaños:
        with open(f"datos/peliculas_{n}.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            lista_datos = [Pelicula(**item) for item in datos]

        print(heap_vs_sorted(lista_datos))

if __name__ == "__main__":
    main()