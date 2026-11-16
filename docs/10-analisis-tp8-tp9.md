# Análisis TP8 + TP9 — DFS y BFS + caminos mínimos

## 1. ¿Qué resolvimos?

En esta etapa incorporamos tres tipos de recorridos de grafos que resuelven problemas distintos dentro del sistema:

| Recorrido | Problema que resuelve | Dónde se usa |
| :--- | :--- | :--- |
| **DFS** | Obtención sencilla de la maratón de películas relacionadas | Opción "Películas relacionadas por género/director" del menú |
| **BFS** | Obtener el camino más corto entre dos películas | Opción "Encontrar camino entre dos películas" del menú |
| **Dijkstra** | Obtener el camino más conveniente entre dos películas | Opción "Encontrar camino entre dos películas" del menú |

---

## 2. TP8 — DFS y BFS
### 2.1 ¿Por qué usar estos recorridos?

DFS fue utilizado para obtener de manera sencilla una lista de películas para ver al estilo maratón a partir de una cierta película de origen. Esto estaba ya presente desde la entrega anterior al crear los grafos (pero no era el elemento central de la misma).
Se agregó un nuevo uso de BFS (distinto a la obtención de los vecinos directos), que se utilizó para encontrar el camino con menos aristas en el grafo entre dos películas. Es importante notar que este no es necesariamente el camino más conveniente. La función permite encontrar una transición rápida entre dos películas a través de aquellas otras con las que compartan características.

### 2.3 Código de las funciones de recorrido

Archivo: estructuras/grafos.py

* dfs: implementación de la búsqueda en profundidad.
* bfs: implementación de la búsqueda en anchura.
* bfs_camino_mas_corto: implementación especial de la búsqueda en anchura que devuelve la lista de los elementos en el camino entre dos elementos en el grafo (si lo hay).

---

## 3. TP9 — Caminos mínimos

### 3.1 ¿Cómo lo integramos?

Se decidió definir un "costo" para las relaciones entre películas, de modo en que se pueda recorrer el grafo de relaciones según la conveniencia/afinidad. Para las películas relacionadas (las que comparten género y/o director según la consideración actual), el costo de ir de una película A a otra película B fue definido de la siguiente manera:
$$costo(A,B) = penalización + |A.rating - B.rating| + \frac{|A.anio - B.anio|}{10} $$
de modo que se suavizan las diferencias de rating y los saltos de época, y en donde la penalización es según el nivel de vínculo que tienen:
- 0,5 si comparten director y género (la mejor transición).
- 1,0 si solo comparten director.
- 2,0 si solo comparten género.

Al definirlo así, nunca se obtienen pesos negativos. Debido a esto, fue posible utilizar el algoritmo de Dijkstra para encontrar los caminos buscados.

### 3.2 ¿Para qué se utiliza?

Se decidió utilizar el algoritmo de Dijkstra sobre la versión ponderada del grafo de películas relacionadas (que también se agregó en esta entrega) para complementar la opción del camino entre dos películas que utiliza BFS descrita en la parte anterior; la idea fue que el usuario pueda elegir si quiere el camino más corto o el más conveniente (de acuerdo al criterio de costo definido anteriormente). Un caso interesante para hacer la prueba es el camino entre Porco Rosso y La Monja.

### 3.3 Código del grafo ponderado y de Dijkstra

Archivo: estructuras/grafos.py
* GrafoPonderado: implementación del grafo no dirigido ponderado.
* Métodos del grafo: agregar_vertice, agregar_arista, mostrar.
* dijkstra: implementación del algoritmo de Dijkstra.

---

## 4. Integración con la aplicación

### 4.1 ¿Dónde quedan los recorridos?

| Interfaz de terminal | |
| :---: | :---: |
| **Opción 6: Películas relacionadas por género/director**<br><br>usa: DFS | **Opción 9: Encontrar camino entre dos películas**<br><br>usa: BFS y Dijkstra |

### 4.2 Código de integración en servicios/gestor_películas.py

**Import:**
```python
from estructuras.grafos import Grafo, dfs, GrafoPonderado, bfs_camino_mas_corto, dijkstra
```

**Inicialización:**
```python
with open(ruta, "r", encoding = "utf-8") as archivos:
    datos = json.load(archivos)
    self._peliculas = [Pelicula(d["id"], d["titulo"], d["director"], d["genero"], d["rating"], d["anio"]) for d in datos]
    
    raiz_categorias = self._arbol_categorias.insertar_raiz("Categorías")
    por_genero = {}
    por_director = {}
    
    for p in self._peliculas:
        self._arbol_anio.insertar(p, clave = lambda e: e.anio)
        self._avl_titulo.insertar(p, clave = lambda e: e.titulo.lower())
        self._bst_director.insertar(p, clave = lambda e: e.director)
        self._bst_genero.insertar(p, clave = lambda e: e.genero)
        genero = p.genero
        if genero not in self.generos:
            nodo_g = self._arbol_categorias.agregar_hijo(raiz_categorias, genero)
            self.generos[genero] = nodo_g
        self._arbol_categorias.agregar_hijo(self.generos[genero], p)
        self._heap_ratings.insertar((p.rating, p.titulo, p))
        
        self._grafo_relacionadas.agregar_vertice(p)
        self._grafo_ponderado.agregar_vertice(p)
        g_key = p.genero.lower().strip()
        d_key = p.director.lower().strip()

        if g_key not in por_genero:
            por_genero[g_key] = []
        por_genero[g_key].append(p)
        
        if d_key not in por_director:
            por_director[d_key] = []
        por_director[d_key].append(p)

    for grupo in por_genero.values():
        for i in range(len(grupo)):
            for j in range(i + 1, len(grupo)):
                self._grafo_relacionadas.agregar_arista(grupo[i], grupo[j])
                costo = self._calcular_costo_transicion(grupo[i], grupo[j])
                self._grafo_ponderado.agregar_arista(grupo[i], grupo[j], costo)

    for grupo in por_director.values():
        for i in range(len(grupo)):
            for j in range(i + 1, len(grupo)):
                if grupo[j] not in self._grafo_relacionadas.vertices[grupo[i]]:
                    self._grafo_relacionadas.agregar_arista(grupo[i], grupo[j])
                    costo = self._calcular_costo_transicion(grupo[i], grupo[j])
                    self._grafo_ponderado.agregar_arista(grupo[i], grupo[j], costo)
```

**Opción "Encontrar camino entre dos películas":**

```python
    def buscar_camino_mas_corto(self, origen, destino):
        """Devuelve el camino con menor cantidad de saltos usando BFS"""
        return bfs_camino_mas_corto(self._grafo_relacionadas.vertices, origen, destino)

    def buscar_camino_recomendado(self, origen, destino):
        """Devuelve el camino de menor costo acumulado y su costo total usando Dijkstra"""
        return dijkstra(self._grafo_ponderado.vertices, origen, destino)
```

**Opción "Películas relacionadas por género/director":**

```python
def obtener_relacionadas(self, pelicula, maraton = False):
    """Devuelve las películas relacionadas por género o por director (utilizando un grafo),
    puede devolver también una 'maratón' de 4 películas obtenida por DFS"""
    relacionadas = self._grafo_relacionadas.vertices[pelicula]
    maraton_propuesta = []
    if maraton:
        camino_dfs = dfs(self._grafo_relacionadas.vertices, pelicula)
        maraton_propuesta = camino_dfs[:4]
    return relacionadas, maraton_propuesta
```

---

## 5. Conclusión

* **El montículo máximo** garantiza búsquedas eficientes sin importar la cantidad de películas solicitadas o si la base de datos es muy grande, a diferencia del método implementado anteriormente.
* **El grafo no dirigido** permite organizar el dominio de acuerdo a las relaciones entre películas de una mejor manera, permitiendo devolver una mejor búsqueda de películas relacionadas y la implementación del sistema de sugerencias.
* Ninguna de las dos se usó "por cumplir": el MaxHeap resuelve un problema real (eficiencia de búsqueda) y el Grafo resuelve otro (relación de los elementos del dominio).

---

## 6. Problemas que tuvimos y resolución

### 6.1 BFS especial

Como queríamos usar la BFS para obtener el camino entre dos puntos y no solo obtener el resultado, creamos una implementación especial para este fin:

```python
def bfs_camino_mas_corto(grafo, origen, destino):
    if origen == destino:
        return [origen]
    visitados = {origen}
    cola = [[origen]]

    while cola:
        camino = cola.pop(0)
        actual = camino[-1]
        for vecino in grafo[actual]:
            if vecino not in visitados:
                nuevo_camino = camino + [vecino]
                if vecino == destino:
                    return nuevo_camino
                visitados.add(vecino)
                cola.append(nuevo_camino)
    return []
```

### 6.2 Cálculo del costo/peso

Teníamos que tener alguna manera de definir y calcular el costo para crear el grafo ponderado, así que lo planteamos con la lógica descrita antes y la función de su implementación quedó así y es parte de la clase GestorPelículas.

```python
def _calcular_costo_transicion(self, p1, p2):
    """Calcula el costo no negativo de pasar de la película p1 a p2"""
    mismo_genero = p1.genero.lower().strip() == p2.genero.lower().strip()
    mismo_director = p1.director.lower().strip() == p2.director.lower().strip()

    if mismo_genero and mismo_director:
        penalizacion_vinculo = 0.5
    elif mismo_director:
        penalizacion_vinculo = 1.0
    else:
        penalizacion_vinculo = 2.0

    dif_rating = abs(p1.rating - p2.rating)
    dif_anio = abs(p1.anio - p2.anio) / 10.0
    return round(penalizacion_vinculo + dif_rating + dif_anio, 2)
```

# 6.3 Grafo ponderado

Para poder implementar el algoritmo de Dijkstra a partir de las relaciones entre películas con pesos, se tuvo que definir una clase de grafos ponderados modificando un poco la clase Grafo que teníamos originalmente. Quedó así:

```python
class GrafoPonderado:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, valor):
        if valor not in self.vertices:
            self.vertices[valor] = {}

    def agregar_arista(self, v_desde, v_hasta, peso = 1.0):
        if v_desde in self.vertices and v_hasta in self.vertices:
            self.vertices[v_desde][v_hasta] = peso
            self.vertices[v_hasta][v_desde] = peso
        else:
            raise ValueError("Vértice inválido")

    def mostrar(self):
        for vertice in self.vertices:
            print(f"{vertice} -> ", end = "")
            vecinos = self.vertices[vertice]
            if vecinos:
                for vecino, peso in vecinos.items():
                    print(f"{vecino} ({peso}) -> ", end = "")
            print("None")
```

# 6.4 Base de datos

Notamos que las relaciones entre películas al tener una base de solo 20 elementos no eran muchas, por lo que se dificultaba evaluar el funcionamiento de la obtención del camino más conveniente. Por lo tanto, se decidió ampliar la base de datos hasta un total de 500 películas.

---