# Análisis TP3 — Árbol Binario de Búsqueda

## 1. ¿Qué resolvimos?
Incorporamos un **árbol binario de búsqueda (BST)** para resolver la
búsqueda por año de forma más eficiente.

## 2. Clave de ordenamiento
La clave de ordenamiento seleccionada fue el año de estreno de cada película, puesto que era lo más apropiado para crear el BST para una búsqueda según esta característica.

## 3. Prueba del árbol
Salida de `python algoritmos/probar_bst.py`:

Altura del árbol: 4                                               

--- inorder (ordenado alfabéticamente) ---
  Arrival (2016) - ciencia ficcion - 8.4/10 - Dirigida por Villenueve
  Blade Runner 2049 (2017) - ciencia ficcion - 8.0/10 - Dirigida por Villenueve
  Inception (2010) - ciencia ficcion - 9.0/10 - Dirigida por Nolan
  Matrix (1999) - ciencia ficcion - 9.1/10 - Dirigida por Wachowski
  Titanic (1997) - drama - 7.8/10 - Dirigida por Cameron

--- preorder ---
  Matrix
  Inception
  Blade Runner 2049
  Arrival
  Titanic

--- postorder ---
  Arrival
  Blade Runner 2049
  Inception
  Titanic
  Matrix

--- búsquedas ---
Buscar 'matrix': [Matrix (1999) - ciencia ficcion - 9.1/10 - Dirigida por Wachowski]
Buscar 'zzz': []

## 4. Comparación de tiempos
En la tabla siguiente, los tiempos son **reales**, sacados con nuestro
script `algoritmos/medir_tiempos.py`.
| N elementos | Secuencial (ms) | Binaria (ms) | Árbol BST (ms) |
|---|---:|---:|---:|
| 100 | 0,0047 | 0,0055 | 0,0015 |
| 1.000 | 0,0470 | 0,0581 | 0,0031 |
| 10.000 | 0,6873 | 0,7946 | 0,0213 |
| 100.000 | 19,6463 | 23,9142 | 0,2911 |

## 5. Análisis de complejidad
- **Búsqueda secuencial:** O(n). Recorre toda la lista en el peor caso.
- **Búsqueda binaria:** O(log n) pero exige lista ordenada (ordenar cuesta O(n log n))
- **Búsqueda en árbol:** O(log n) promedio si el árbol está balanceado; O(n) en el peor caso si está degenerado (como una lista).
- **Inserción en árbol:** O(log n) promedio, O(n) peor caso.
- **Recorridos (inorder, preorder, postorder):** O(n), porque visitan cada nodo 1 vez.

## 6. Conclusión
Puede evidenciarse en la tabla del punto 4 que para este uso que se implementó, la búsqueda mediante el árbol es mucho más eficiente que los otros dos métodos, especialmente cuando tenemos una cantidad de datos mayor (en donde los efectos se intensifican).
Se observa que con 100.000 elementos la secuencial tarda 19,6463 ms y el árbol 0,2911 ms. El árbol conviene para búsquedas frecuentes; el costo de construir el árbol se paga una sola vez. Eventualmente, tal vez sea adecuado implementar el árbol binario para las otras búsquedas que incluimos en la herramienta (por título y por director).

## 7. Errores o dudas que tuvimos
El código de árbol binario de búsqueda que se nos había proporcionado solo implementaba una búsqueda que devolvía un elemento (o el primero que coincidiera con la característica buscada), pero notamos que esto no era lo ideal para buscar todas las películas correspondientes a un año en particular. Observamos que la definición de la estructura del árbol hacía que los elementos con año repetido se coloquen a la derecha del elemento del mismo año insertado previamente, por lo que únicamente cambiamos la definición de la búsqueda para que devolviera una lista con todas las coincidencias, y quedó del siguiente modo:

```python
def buscar(self, valor, clave):
        """Busca por valor. Devuelve una lista con todos los elementos coincidentes o None si no existe."""
        resultados = []
        self._buscar_recursivo(self.raiz, valor, clave, resultados)
        return resultados

    def _buscar_recursivo(self, nodo, valor, clave, resultados):
        if nodo is None:
            return None

        val_nodo = clave(nodo.dato)
        
        if valor == val_nodo:
            resultados.append(nodo.dato)
            self._buscar_recursivo(nodo.derecho, valor, clave, resultados)
        elif valor < val_nodo:
            self._buscar_recursivo(nodo.izquierdo, valor, clave, resultados)
        else:
            self._buscar_recursivo(nodo.derecho, valor, clave, resultados)
```