import timeit
from estructuras.arbol_binario import ArbolBST
from servicios.gestor_peliculas import GestorPeliculas

def crear_arbol(lista):
    """Llena el árbol para poder hacer la medición."""
    arbol = ArbolBST()
    for e in lista:
        arbol.insertar(e, clave = lambda e: e.anio)
    return arbol

def main() -> None:
    tamaños = (100, 1000, 10000, 100000)
    print("tamaño\tsecuencial_ms\tbinaria_ms\tbst_ms")
    for n in tamaños:
        gestor = GestorPeliculas()
        gestor.cargar_desde_json(f"datos/peliculas_{n}.json")
        arbol = crear_arbol(gestor._peliculas)
        anio_probe = gestor._peliculas[len(gestor._peliculas) - 1].anio # existe → no rompe el caso "no encontrado"
        gestor.ordenar_por_anio()
        t_sec = min(timeit.repeat(lambda: gestor.buscar_por_anio_sec(anio_probe), number = 20, repeat = 5)) / 20 * 1000
        t_bin = min(timeit.repeat(lambda: gestor.buscar_binaria(anio_probe), number = 20, repeat = 5)) / 20 * 1000
        t_bst = min(timeit.repeat(lambda: arbol.buscar(anio_probe, lambda e: e.anio), number = 20, repeat = 5)) / 20 * 1000
        print(f"{n}\t{t_sec:.4f}\t\t{t_bin:.4f}\t\t{t_bst:.4f}")

if __name__ == "__main__":
    main()