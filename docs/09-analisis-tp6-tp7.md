# Análisis TP6 + TP7 — Heap y Grafos

## 1. ¿Qué resolvimos?

En esta etapa incorporamos **dos estructuras de datos** que resuelven problemas distintos dentro del sistema:

| Estructura | Problema que resuelve | Dónde se usa |
| :--- | :--- | :--- |
| **MaxHeap** | Que la búsqueda del top N mejores películas sea rápida, especialmente cuando aumenta el tamaño de la base de datos | Opción "Top N mejores películas" del menú |
| **Grafo** | Mejorar la función de películas relacionadas para que no solo considere el género al buscar y para agregar sugerencias | Opción "Películas relacionadas por género/director" del menú |

---

## 2. TP6 — Heap
### 2.1 ¿Por qué usar un montículo?

En la implementación anterior, para obtener las N mejores películas según el rating se estaba utilizando el método sorted de Python para ordenar todas las películas en una lista y luego se hacía slicing para obtener las N primeras en esa lista ordenada. Este método es ineficiente para listas grandes en comparación con la implementación actual, que utiliza un montículo máximo (ordenado por rating) que se genera al cargar los datos para extraer de él los valores necesarios.

**Datos de prueba:**
Utilizamos nuevamente los datos generados a través del script datos/generar.py para el resto de los test.

### 2.2 Comparación MaxHeap vs sorted

Se realizó la llamada al método del top N en nuestra clase MaxHeap y se comparó con lo que se tarda en hallar el mismo top N a través del método anterior. Se define un numero al azar entre 3 y 15 de películas a retornar, y se compara el tiempo en milisegundos con distintos tamaños de base de datos.

| Cantidad de películas | MaxHeap (ms) | sorted (ms) |
| :--- | :--- | :--- |
| 100 | 14,7 | 9,5 |
| 1000 | 33,5 | 109,1 |
| 10000 | 61,0 | 1495,7 |
| 100000 | 632,6 | 18203,1 |

### 2.3 Código de la clase MaxHeap

Archivo: estructuras/heaps.py

* MinHeap: implementación del montículo mínimo.
* MaxHeap: implementación del montículo máximo.
* Métodos públicos: esta_vacio, insertar, consultar_maximo, extraer_maximo, obtener_top_n.

---

## 3. TP7 — Grafos

### 3.1 ¿Cómo se integra el grafo?

Se decidió incorporar un grafo para rediseñar la función de las películas relacionadas. Se incluyeron implementaciones de grafo dirido y grafo no dirigido. En este caso, se crea un grafo no dirigido al cargar los datos en el que cada película es un vértice, y tiene aristas que la conecta con otras siempre que compartan género o director.

### 3.2 ¿Por qué este cambio?

Con la implementación anterior solo se obtenían las películas que compartían el género, pero de este modo se logra una funcionalidad ampliada en la que también se tiene en cuenta el director (dado que normalmente se considera que dos películas están relacionadas si fueron dirigidas por la misma persona). Cuando se buscan las películas relacionadas a una en particular se devuelven sus vecinos, lo que es (aunque de manera muy reducida) un recorrido por amplitud.
Además, esto permitió agregar una función que le sugiere al usuario una "maratón" de 4 películas relacionadas para ver en sucesión. Esto se logra mediante un recorrido por profundidad.

### 3.3 Recorridos implementados

| Recorrido | Descripción | Complejidad |
| :--- | :--- | :--- |
| **Amplitud (BFS)** | Acceso directo a los vecinos de distancia 1 utilizando la lista de adyacencia del grafo.. Se utilizó para obtener las películas relacionadas directamente. | O(1) + O(n_vecinos) |
| **Profundidad (DFS)** | Explora el grafo en profundidad avanzando lo más lejos posible por cada rama antes de retroceder. Se utilizó para generar la sugerencia de maratón. | O(V+E) |

### 3.4 Código del grafo

Archivo: estructuras/grafos.py
* Grafo: implementación del grafo no dirigido.
* Digrafo: implementación del grafo dirigido.
* Métodos de los grafos: agregar_vertice, agregar_arista_mostrar.
* Funciones de recorridos: bfs, dfs.

---

## 4. Integración con la aplicación

### 4.1 ¿Dónde queda la estructura?

| Interfaz de terminal | |
| :---: | :---: |
| **Opción 7: Top N mejores películas**<br><br>usa: MaxHeap | **Opción 6: Películas relacionadas por género/director**<br><br>usa: Grafo |

### 4.2 Código de integración en servicios/gestor_películas.py

**Import:**
```python
from estructuras.heaps import MaxHeap
from estructuras.grafos import Grafo, dfs
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
        self._avl_titulo.insertar(p, clave = lambda e: e.titulo)
        self._bst_director.insertar(p, clave = lambda e: e.director)
        self._bst_genero.insertar(p, clave = lambda e: e.genero)
        genero = p.genero
        if genero not in self.generos:
            nodo_g = self._arbol_categorias.agregar_hijo(raiz_categorias, genero)
            self.generos[genero] = nodo_g
        self._arbol_categorias.agregar_hijo(self.generos[genero], p)
        self._heap_ratings.insertar((p.rating, p.titulo, p))
        
        self._grafo_relacionadas.agregar_vertice(p)
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

    for grupo in por_director.values():
        for i in range(len(grupo)):
            for j in range(i + 1, len(grupo)):
                if grupo[j] not in self._grafo_relacionadas.vertices[grupo[i]]:
                    self._grafo_relacionadas.agregar_arista(grupo[i], grupo[j])
```

**Opción "Top N mejores películas":**

```python
def obtener_top_n_mejores(self, n):
    """Devuelve una lista con las N mejores películas (utilizando un montículo máximo)"""
    tuplas_top = self._heap_ratings.obtener_top_n(n)

    return [tupla[2] for tupla in tuplas_top]
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

### 6.1 Obtención de los N elementos superiores del montículo sin modificarlo

Para poder hacer más sencillo el proceso de mostrar los N primeros elementos en salir del montículo, se tuvo que agregar un método adicional "obtener_top_n" que típicamente no se incluye en la implementación de los montículos máximos. Quedó del siguiente modo:

```python
def obtener_top_n(self, n):
    """Devuelve los N elementos mayores sin destruir ni modificar el heap"""
    if n <= 0 or self.esta_vacio():
        return []
        
    heap_aux = MaxHeap()
    heap_aux._elementos = list(self._elementos)
    
    resultado = []
    for _ in range(min(n, len(heap_aux))):
        resultado.append(heap_aux.extraer_maximo())
        
    return resultado
```

Para mantener todo completo, se añadió un método similar a la definición de la clase del montículo mínimo:

```python
    def obtener_n_minimos(self, n):
    """Devuelve los N elementos menores sin destruir ni modificar el heap principal"""
    if n <= 0 or self.esta_vacio():
        return []

    heap_aux = MinHeap()
    heap_aux._elementos = list(self._elementos)
    
    resultado = []
    for _ in range(min(n, len(heap_aux))):
        resultado.append(heap_aux.extraer_minimo())
        
    return resultado
```

### 6.2 Implementación del grafo no dirigido

Para poder relacionar las películas, se modificó el código de grafos provisto por el docente, que formaba un grafo dirigido, para formar un grafo no dirigido. En cuanto a lo que son relaciones entre películas, no existe una direccionalidad. Se modificó el añadido de aristas, que pasó de realizarse del modo

```python
def agregar_arista(self, v_desde, v_hasta):
    if v_desde in self.vertices and v_hasta in self.vertices:
        if v_hasta not in self.vertices[v_desde]:
            self.vertices[v_desde].append(v_hasta)
    else:
        raise ValueError("Vértice inválido")
```

a hacerse de la forma

```python
def agregar_arista(self, v_desde, v_hasta):
    if v_desde in self.vertices and v_hasta in self.vertices:
        if v_hasta not in self.vertices[v_desde]:
            self.vertices[v_desde].append(v_hasta)
        if v_desde not in self.vertices[v_hasta]:
            self.vertices[v_hasta].append(v_desde)
    else:
        raise ValueError("Vértice inválido")
```

para quitar la direccionalidad. El código original se conservó y se utilizó para definir la clase Digrafo.

---

## 7. Datos y evidencia
* Script de comparación del MaxHeap con el método previo (utilizando sorted): [heap_vs_sorted.py](../algoritmos/probar_avl.py)
* Salidas de scripts de prueba: [tests](../tests/)

