def comparar_bst_vs_avl(lista_datos, clave):
    """Compara un BST común con un AVL insertando los mismos datos.

    Retorna un diccionario con las alturas de ambos árboles y
    tiempos de búsqueda para demostrar la diferencia de desbalance.
    """
    import time
    import random
    from estructuras.arbol_binario import ArbolBST
    from estructuras.avl import AVL

    bst = ArbolBST()
    for d in lista_datos:
        bst.insertar(d, clave=clave)

    # --- AVL ---
    avl = AVL()
    for d in lista_datos:
        avl.insertar(d, clave=clave)

    # Medir tiempo de búsqueda en ambos
    valor_test = clave(random.choice(lista_datos))

    inicio = time.time()
    for _ in range(1000):
        bst.buscar(valor_test, clave=clave)
    tiempo_bst = (time.time() - inicio) * 1000

    inicio = time.time()
    for _ in range(1000):
        avl.buscar(valor_test, clave=clave)
    tiempo_avl = (time.time() - inicio) * 1000

    return {
        "altura_bst": bst.altura(),
        "altura_avl": avl.altura(),
        "tiempo_bst_ms": tiempo_bst,
        "tiempo_avl_ms": tiempo_avl,
        "mejor_balance": avl.altura() < bst.altura(),
    }

def main() -> None:
    import json
    from modelos.pelicula import Pelicula
    
    tamaños = (100, 1000, 10000, 100000)
    for n in tamaños:
        with open(f"datos/peliculas_{n}.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            lista_datos = [Pelicula(**item) for item in datos]

        print(comparar_bst_vs_avl(lista_datos, lambda e: e.titulo))

if __name__ == "__main__":
    main()