from servicios.gestor_peliculas import GestorPeliculas

class InterfazTerminal:
    def __init__(self):
        self.gestor = GestorPeliculas()

    def mostrar_menu(self):
        """Muestra por pantalla el título y el menú de opciones"""
        print("\n" + "=" * 36)
        print("        ¡Bienvenido a Kino!")
        print("=" * 36)
        print("1. Mostrar todas las películas")
        print("2. Buscar por título")
        print("3. Buscar por director")
        print("4. Filtrar por género")
        print("5. Películas relacionadas")
        print("6. Top N mejores películas")
        print("0. Salir")
        print("\n")

    def iniciar(self):
        """Carga los datos e inicia el loop principal del menú"""
        self.gestor.cargar_desde_json()
        
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                print("\nColección de películas completa:")
                self.gestor.mostrar_peliculas()

            elif opcion == "2":
                titulo = input("Ingrese el titulo de la película: ").strip()
                resultado = self.gestor.buscar_por_titulo(titulo)
                 
                if resultado:
                    print("\nPelículas encontradas:")
                    for i, pelicula in enumerate(resultado, 1):
                        print(f"{i}. {pelicula}")
                else:
                    print("\nNo se encontraron películas con ese título.")
                
            elif opcion == "3":
                director = input("Ingrese nombre del director: ").strip()
                resultado = self.gestor.buscar_por_director(director)
               
                if resultado:
                    print("\nPelículas encontradas:")
                    for i, pelicula in enumerate(resultado, 1):
                        print(f"{i}. {pelicula}")
                else:
                    print("\nNo se encontraron películas con ese director.")
                
            elif opcion == "4":
                genero = input("Ingrese el género: ").strip()
                resultado = self.gestor.buscar_por_genero(genero)
               
                if resultado:
                    print("\nPelículas encontradas:")
                    for i, pelicula in enumerate(resultado, 1):
                        print(f"{i}. {pelicula}")
                else:
                    print("\nNo se encontraron películas con ese género.")
                
            elif opcion == "5":
                titulo = input("Ingrese el título de la película base: ")
                encontradas = self.gestor.buscar_por_titulo(titulo)
            
                if not encontradas:
                    print(f"No se encontró ninguna película con el nombre '{titulo}'.")
                    return
                
                pelicula_base = encontradas[0]
                print(f"Película seleccionada: {pelicula_base}")
                
                relacionadas = self.gestor.obtener_relacionadas(pelicula_base)
                if relacionadas:
                    print(f"\nPelículas relacionadas por género ({pelicula_base.genero}):")
                    for p in relacionadas:
                        print(f" - {p}")
                else:
                    print("No se encontraron otras películas relacionadas en el catálogo.")

            elif opcion == "6":
                n = int(input("¿Cuantas películas desea mostrar? Ingrese el número: "))
                resultado = self.gestor.obtener_top_n_mejores(n)
                 
                if resultado:
                    print("\nTop N mejores películas:")
                    for i, pelicula in enumerate(resultado, 1):
                        print(f"{i}. {pelicula}")
                else:
                    print("\nNo se encontraron películas que cumplan con los criterios.")
               
            elif opcion == "0":
                print("\n¡Gracias por usar Kino! Hasta luego")
                break
            else:
                print("\n[!] Opción no válida. Por favor, intente de nuevo")