# Análisis TP4 + TP5 — AVL y Árbol General

## 1. ¿Qué resolvimos?

En esta etapa incorporamos **dos estructuras de datos** que resuelven problemas distintos dentro del sistema:

| Estructura | Problema que resuelve | Dónde se usa |
| :--- | :--- | :--- |
| **AVL** | Que las búsquedas por título sean siempre rápidas (O(log n)) incluso cuando los datos se insertan en orden | Opción "Buscar por título" del menú |
| **Árbol General** | Representar la jerarquía de las películas según el género | Opción "Mostrar categorías disponibles" del menú |

---

## 2. TP4 — Árbol AVL
### 2.1 ¿Por qué AVL y no un BST común?

Un BST común se desbalancea cuando se insertan datos ordenados (ej: títulos en orden alfabético). Esto lo convierte en una lista enlazada con complejidad O(n) por búsqueda. El AVL resuelve esto con **rotaciones automáticas** que mantienen la altura en O(log n) sin importar el orden de inserción.

### 2.2 Rotaciones implementadas

| Tipo | Caso | Cuándo se aplica |
| :--- | :--- | :--- |
| Rotación simple derecha | Izquierda-<br>Izquierda | Factor de balance > 1 y el nuevo dato va a la izquierda del hijo izquierdo |
| Rotación simple izquierda | Derecha-<br>Derecha | Factor de balance < -1 y el nuevo dato va a la derecha del hijo derecho |
| Rotación doble izquierda-derecha | Izquierda-<br>Derecha | Factor de balance > 1 pero el hijo izquierdo está desbalanceado a la derecha |
| Rotación doble derecha-izquierda | Derecha-<br>Izquierda | Factor de balance < -1 pero el hijo derecho está desbalanceado a la izquierda |

### 2.3 Casos de desbalance generados

Insertamos datos **en orden alfabético** (escenario que rompe un BST común) y demostramos que el AVL mantiene la altura controlada.

**Datos de prueba:**
Utilizamos datos generados a través del script datos/generar.py, insertados en orden usando como clave el título de las películas.

### 2.4 Comparación BST vs AVL

| Métrica | BST común | AVL |
| :--- | :--- | :--- |
| Altura con 100.000 datos ordenados | 50 | 19 |
| Búsqueda con 100.000 datos ordenados | 5.001 ms | 3.001 ms |
| Complejidad peor caso búsqueda | O(n) | O(log n) |
| Complejidad promedio inserción | O(log n) | O(log n) |

### Prueba del AVL

Salida de ```python -m estructuras.avl```:

```text
=== AVL con datos ordenados ===
Altura del AVL: 4
Cantidad de nodos: 10

--- inorder ---
  A(1)
  B(2)
  C(3)
  D(4)
  E(5)
  F(6)
  G(7)
  H(8)
  I(9)
  J(10)

--- preorder (muestra el balance) ---
  D(4)
  B(2)
  A(1)
  C(3)
  H(8)
  F(6)
  E(5)
  G(7)
  I(9)
  J(10)

Buscar 'F': F(6)
Buscar 'Z': None
```

### 2.6 Código del AVL

Archivo: estructuras/avl.py

* NodoAVL: nodo con dato, hijos y altura.
* AVL: árbol con inserción balanceada, búsqueda y recorridos.
* Rotaciones: _rotacion_izquierda, _rotacion_derecha, _rotacion_izquierda_derecha, _rotacion_derecha_izquierda.

---

## 3. TP5 — Árbol General (N-ario)

### 3.1 ¿Qué es un árbol general?

A diferencia del árbol binario donde cada nodo tiene máximo 2 hijos, un **árbol general** permite que cada nodo tenga **cualquier cantidad de hijos**. Esto lo hace ideal para representar jerarquías naturales.

### 3.2 Jerarquía elegida del dominio

```text
Categorías
 └─Ciencia ficcion
  └─Matrix
  └─Inception
  └─Interstellar
  └─Volver al futuro
  └─Blade Runner 2049
 └─Animacion
  └─Toy Story
  └─El viaje de Chihiro
  └─Shrek
  └─WALL-E
 └─Drama
  └─El padrino
  └─El club de la pelea
  └─Whiplash
  └─El secreto de sus ojos
 └─Crimen
  └─Pulp Fiction
  └─Tiempos violentos
 └─Thriller
  └─Parasite
 └─Accion
  └─Gladiador
  └─El caballero de la noche
 └─Terror
  └─Psicosis
 └─Fantasia
  └─El senor de los anillos: El retorno del rey
```

**¿Por qué esta jerarquía?**
* Los géneros son una clasificación natural del dominio.
* Permite al usuario explorar las películas sencillamente a través de la jerarquía.
* Se complementa con el AVL: el AVL busca por título; el árbol general organiza por categoría.

### 3.3 Recorridos implementados

| Recorrido | Descripción | Complejidad |
| :--- | :--- | :--- |
| **Amplitud (BFS)** | Nivel por nivel, de arriba hacia abajo | O(n) |
| **Profundidad preorder** | Nodo → hijos (izquierda a derecha) | O(n) |
| **Profundidad postorder** | Hijos → nodo | O(n) |

### 3.4 Prueba del árbol general

Salida de ```python -m estructuras.arbol_general```:

```text
=== Árbol General de Categorías ===
Raíz: Películas
Altura: 3
Cantidad de nodos: 11

--- Recorrido en amplitud ---
['Películas', 'Ciencia Ficción', 'Acción', 'Comedia', 'Cyberpunk', 'Viajes temporales', 'Inteligencia artificial', 'Superhéroes', 'Guerra', 'Comedia romántica', 'Comedia negra']

--- Recorrido en profundidad (preorder) ---
['Películas', 'Ciencia Ficción', 'Cyberpunk', 'Viajes temporales', 'Inteligencia artificial', 'Acción', 'Superhéroes', 'Guerra', 'Comedia', 'Comedia romántica', 'Comedia negra']

--- Recorrido en profundidad (postorder) ---
['Cyberpunk', 'Viajes temporales', 'Inteligencia artificial', 'Ciencia Ficción', 'Superhéroes', 'Guerra', 'Acción', 'Comedia romántica', 'Comedia negra', 'Comedia', 'Películas']

--- Niveles ---
  Nivel 0: ['Películas']
  Nivel 1: ['Ciencia Ficción', 'Acción', 'Comedia']
  Nivel 2: ['Cyberpunk', 'Viajes temporales', 'Inteligencia artificial', 'Superhéroes', 'Guerra', 'Comedia romántica', 'Comedia negra']

--- Hijos de 'Ciencia Ficción' ---
['Cyberpunk', 'Viajes temporales', 'Inteligencia artificial']

--- Buscar 'Cyberpunk' ---
Encontrado: Nodo(Cyberpunk)
```

### 3.5 Código del árbol general

Archivo: estructuras/arbol_general.py
* NodoGeneral: nodo con dato y lista de hijos.
* ArbolGeneral: árbol con inserción, búsqueda y recorridos.
* Métodos: insertar_raiz, agregar_hijo, buscar, amplitud, profundidad_preorder, profundidad_postorder.

---

## 4. Integración con la aplicación

### 4.1 ¿Dónde queda la estructura?

| Interfaz de terminal | |
| :---: | :---: |
| **Opción 2: Buscar por título**<br><br>usa: AVL | **Opción 8: Mostrar categorías disponibles**<br><br>usa: Árbol general |

### 4.2 Código de integración en servicios/gestor_películas.py

**Import:**
```python
from estructuras.avl import AVL
from estructuras.arbol_general import ArbolGeneral
```

**Inicialización:**
```python
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
```

**Opción "Buscar por título":**

```python
def buscar_por_titulo(self, titulo):
    """Busca películas según el título ingresado (utilizando un AVL)"""
    titulo_lower = titulo.lower().strip()
    return [self._avl_titulo.buscar(titulo_lower, lambda e: e.titulo.lower())] if self._avl_titulo.buscar(titulo_lower, lambda e: e.titulo.lower()) else []
```

**Opción "Mostrar categorías disponibles":**

```python
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
```

---

## 5. Análisis de complejidad

| Operación | AVL | Árbol General |
| :--- | :--- | :--- |
| Inserción | O(log n) | O(1) (agregar hijo a un nodo conocido) |
| Búsqueda | O(log n) | O(n) (recorrido completo) |
| Recorrido inorder | O(n) | O(n) |
| Recorrido amplitud | O(n) | O(n) |
| Altura (peor caso) | O(log n) | O(n) (árbol degenerado) |

### ¿Por qué el AVL es O(log n)?

El AVL mantiene el factor de balance entre -1 y +1 en cada nodo. Esto garantiza que la altura siempre sea proporcional a log₂(n). Un árbol con 1000 nodos tiene altura máxima ~10, vs ~1000 en un BST degenerado.

### ¿Por qué el árbol general no se auto-balancea?

El árbol general no necesita balanceo porque no tiene criterio de ordenamiento. Su estructura refleja una jerarquía natural, no un orden numérico o alfabético. El costo de búsqueda O(n) es aceptable porque la cantidad de categorías suele ser pequeña (decenas, no miles).

---

## 6. Conclusión

* **El AVL** garantiza búsquedas eficientes sin importar el orden de inserción, resolviendo el problema principal de desbalance del BST.
* **El árbol general** permite organizar el dominio en jerarquías significativas que mejoran la experiencia del usuario al explorar categorías.
* Ambas estructuras se complementan: el AVL resuelve búsqueda eficiente por clave, el árbol general organiza la navegación por categorías.
* Ninguna de las dos se usó "por cumplir": el AVL resuelve un problema real (desbalance) y el árbol general resuelve otro (jerarquización del dominio).

---

## 7. Problemas que tuvimos y resolución

### 7.1 Entradas duplicadas

Se encontró un problema al intentar implementar el AVL para otras de las opciones en el programa (como la búsqueda por año), dado que tienen entradas duplicadas y estas no se cargan en el AVL. Es decir, si dos películas comparten el mismo año de estreno el AVL solo conserva la primera al insertar en la implementación actual.
Para las opciones que presentaban este problema se conservó el BST tradicional, insertando los duplicados a la derecha. El AVL quedó unicamente implementado en la búsqueda por título.

### 7.2 Búsqueda con nombres incompletos

Otro cambio que se implementó fue sobre la búsqueda del AVL y del BST para contemplar la posibilidad de las palabras contenidas en el campo usado para filtrar. Por ejemplo, hasta este momento si se buscaba "El senor de los anillos" en vez de "El senor de los anillos: El retorno del rey" la película no era encontrada. En ambas implementaciones se modificó la condición de comparación del siguiente modo:

```python
if valor == valor_nodo or valor in valor_nodo
```

en vez de la condición previamente implementada,

```python
if valor == valor_nodo
```

---

## 8. Datos y evidencia
* Script de prueba del AVL: [avl.py](../estructuras/avl.py)
* Script de prueba del árbol general: [arbol_general.py](../estructuras/arbol_general.py)
* Script de comparación de AVL con BST: [probar_avl.py](../algoritmos/probar_avl.py)
* Salidas de scripts de prueba: [tests](../tests/)
