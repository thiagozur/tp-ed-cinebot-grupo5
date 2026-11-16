# Requerimientos — Kino

## Alcance
Kino es un sistema interactivo con una interfaz en consola que permite buscar, listar y filtrar un catálogo de películas según títulos, géneros o directores, además de obtener recomendaciones de películas relacionadas y rankings de las mejor calificadas. Está pensado para estudiantes universitarios y profesionales jóvenes aficionados al cine que disponen de poco tiempo libre y buscan elegir rápidamente una película alineada a sus gustos sin tener que leer reseñas manualmente.

## Requerimientos funcionales (RF)

| ID | Requerimiento | Estado |
|---|---|---|
| RF01 | El sistema debe permitir buscar una película por título | ✅ TP1 / TP4 |
| RF02 | El sistema debe permitir listar todas las películas o filtrarlas por categoría/género | ✅ TP1 / TP5 |
| RF03 | El sistema debe permitir buscar películas por año de estreno y por director | ✅ TP3 |
| RF04 | El sistema debe mostrar el Top N de películas mejor rankeadas según su puntaje | ✅ TP6 |
| RF05 | El sistema debe mostrar las películas relacionadas con una dada (por género o director) y sugerir una maratón de visualización | ✅ TP7 |
| RF06 | El sistema debe encontrar el camino de menor costo entre dos películas dadas, mostrando la secuencia completa de intermediarios | ✅ TP9 |

### Criterios de aceptación

### Criterios de aceptación

> **RF01 — Búsqueda de película por título**
> - La búsqueda no distingue entre mayúsculas y minúsculas e ignora espacios en los extremos.
> - Devuelve la película coincidente o maneja de manera adecuada la situación cuando no hay resultados.
> - Resuelve consultas en tiempo logarítmico $O(\log n)$ mediante el árbol AVL (3,001 ms con 100.000 datos ordenados).

> **RF02 — Listado general y filtrado por categoría/género**
> - Permite listar la totalidad del catálogo.
> - Permite visualizar las categorías disponibles o el árbol completo de géneros y sus películas asociadas mediante recorrido recursivo del Árbol General.
> - Permite filtrar todas las películas pertenecientes a un género específico.

> **RF03 — Búsqueda por año de estreno y por director**
> - Devuelve una lista con **todas** las películas que coincidan con el año o director buscado, manejando correctamente múltiples registros con la misma clave (duplicados insertados a la derecha en el BST).
> - Si no existen coincidencias para el criterio ingresado, se lo informa al usuario sin interrumpir la ejecución.
> - Con 100.000 elementos, la búsqueda en el BST responde en menos de 1 ms (0,2911 ms medidos).

> **RF04 — Top N mejores películas**
> - Se muestran exactamente $N$ resultados solicitados por el usuario (o el total disponible si el catálogo tiene menos de $N$ películas).
> - Orden descendente por rating; el título define el orden de manera alfabética si hay un empate de rating.
> - La consulta se resuelve sin destruir ni modificar el montículo principal (`MaxHeap`) y responde en menos de 1 segundo con 10.000 elementos (61,0 ms medidos).

> **RF05 — Películas relacionadas y sugerencia de maratón**
> - Dada una película base, se listan todas las películas adyacentes en el grafo no dirigido que compartan género o director, sin duplicados.
> - Opcionalmente, genera una secuencia sugerida de hasta 4 películas conectadas para ver en sucesión mediante recorrido en profundidad (DFS).

> **RF06 — Camino de menor costo entre dos películas** 
> - Dadas dos películas de origen y destino pertenecientes al catálogo, calcula y muestra la secuencia completa de películas intermedias que las conectan por el camino más conveniente.
> - Informa adecuadamente al usuario en caso de que no exista un camino posible entre ambos vértices.

## Requerimientos no funcionales (RNF)

| ID | Requerimiento | Verificación |
|---|---|---|
| RNF01 | La búsqueda por título debe garantizar complejidad logarítmica $O(\log n)$ en el peor caso sobre el total de películas | TP4 (Árbol AVL) |
| RNF02 | El sistema debe soportar al menos 10.000 películas (y escalar hasta 100.000) sin degradar perceptiblemente los tiempos de respuesta | TP3 / TP6 (Benchmarks) |
| RNF03 | La interfaz de terminal debe ser clara, intuitiva y usable mediante menú numérico por alguien que desconoce la implementación interna | Ejemplo de la CLI en la propuesta |
| RNF04 | El proyecto debe ejecutarse en Python 3.10+ utilizando únicamente la biblioteca estándar, sin dependencias externas | README |

## Fuera de alcance
- Autenticación, inicio de sesión o gestión de perfiles de usuario.
- Persistencia de historial, favoritos o preferencias entre sesiones.
- Conexión a APIs externas de cine (IMDb, TMDb) o descarga de datos en tiempo real (el catálogo se carga desde un archivo JSON local).
- Enlaces a opciones de streaming.
- Modificación, alta o baja de películas desde la interfaz de usuario durante la ejecución.

## Observaciones
- **Separación entre AVL y BST para claves duplicadas:** Se optó por utilizar un árbol AVL exclusivamente para la búsqueda por título con el fin de garantizar $O(\log n)$ incluso si los datos ingresan ordenados alfabéticamente. Para las búsquedas por año, director y género se mantuvieron árboles binarios de búsqueda (BST) modificados para insertar claves repetidas hacia la derecha y retornar listas con todas las coincidencias, ya que la implementación del AVL no admite claves duplicadas.
- **Árbol General para jerarquía de categorías:** Se incorporó un árbol N-ario para modelar la relación natural entre géneros y películas, facilitando la exploración estructurada del catálogo.
- **MaxHeap no destructivo para el Top N:** Se reemplazó el ordenamiento completo de listas (`sorted`, $O(n \log n)$) por un montículo máximo con un método auxiliar (`obtener_top_n`) que clona el arreglo interno antes de extraer elementos, preservando la integridad del heap para consultas sucesivas.
- **Grafo no dirigido para recomendaciones:** Se adaptó la estructura de grafo para eliminar la direccionalidad de las aristas, dado que la relación "comparte género o director" es simétrica. Esto permitió resolver tanto las recomendaciones directas (vecinos inmediatos) como la sugerencia de maratones (DFS).
- **Grafo ponderado para Dijkstra:** Se adaptó la estructura de grafo para considerar pesos en las aristas de acuerdo a un costo determinado. Esto permitió encontrar el camino de menor costo entre dos elementos mediante el algoritmo de Dijkstra.