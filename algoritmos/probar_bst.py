from estructuras.arbol_binario import ArbolBST
from modelos.pelicula import Pelicula
    
def main():
    arbol = ArbolBST()
    datos = [
        Pelicula(1, "Matrix", "Wachowski", "ciencia ficcion", 9.1, 1999),
        Pelicula(2, "Inception", "Nolan", "ciencia ficcion", 9.0, 2010),
        Pelicula(21, "Titanic", "Cameron", "drama", 7.8, 1997),
        Pelicula(19, "Blade Runner 2049", "Villenueve", "ciencia ficcion", 8.0, 2017),
        Pelicula(22, "Arrival", "Villenueve", "ciencia ficcion", 8.4, 2016),
    ]
    for d in datos:
        arbol.insertar(d, clave=lambda e: e.titulo.lower())

    print("Altura del árbol:", arbol.altura())

    print("\n--- inorder (ordenado alfabéticamente) ---")
    for e in arbol.inorder():
        print(" ", e)

    print("\n--- preorder ---")
    for e in arbol.preorder():
        print(" ", e.titulo)

    print("\n--- postorder ---")
    for e in arbol.postorder():
        print(" ", e.titulo)

    print("\n--- búsquedas ---")
    encontrado = arbol.buscar("matrix", clave=lambda e: e.titulo.lower())
    print("Buscar 'matrix':", encontrado)
    no_encontrado = arbol.buscar("zzz", clave=lambda e: e.titulo.lower())
    print("Buscar 'zzz':", no_encontrado)

if __name__ == "__main__":
    main()