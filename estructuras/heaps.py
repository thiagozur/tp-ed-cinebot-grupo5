class MinHeap:
    """Implementación de montículo mínimo. Todos los hijos son iguales o mayores al padre"""

    def __init__(self):
        self._elementos = []

    def __len__(self):
        return len(self._elementos)

    def esta_vacio(self):
        """Devuelve True si no hay elementos, y false en el caso contrario"""
        return not self._elementos

    def _intercambiar(self, i_a, i_b):
        self._elementos[i_a], self._elementos[i_b] = self._elementos[i_b], self._elementos[i_a]
    
    def _burbujeo_arriba(self, i):
        while i > 0:
            padre = (i - 1) // 2
            if self._elementos[padre] <= self._elementos[i]:
                break
            self._intercambiar(padre, i)
            i = padre

    def _burbujeo_abajo(self, i):
        n = len(self)
        while True:
            izq = 2 * i + 1
            der = 2 * i + 2
            menor = i
            
            if izq < n and self._elementos[izq] < self._elementos[menor]:
                menor = izq
            if der < n and self._elementos[der] < self._elementos[menor]:
                menor = der
                
            if menor == i:
                break
            self._intercambiar(i, menor)
            i = menor

    def insertar(self, valor):
        """Inserta un elemento nuevo y reordena el montículo"""
        self._elementos.append(valor)
        self._burbujeo_arriba(len(self) - 1)

    def consultar_minimo(self):
        """Devuelve el valor mínimo en el montículo"""
        if self.esta_vacio():
            raise IndexError("El heap está vacío")
        return self._elementos[0]
    
    def extraer_minimo(self):
        """Devuelve el valor mínimo en el montículo, quitándolo"""
        if self.esta_vacio():
            raise IndexError("El heap está vacío")
        
        minimo = self._elementos[0]
        ultimo = self._elementos.pop()

        if not self.esta_vacio():
            self._elementos[0] = ultimo
            self._burbujeo_abajo(0)

        return minimo

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

class MaxHeap:
    """Implementación de montículo máximo. Todos los hijos son iguales o menores al padre"""

    def __init__(self):
        self._elementos = []

    def __len__(self):
        return len(self._elementos)

    def esta_vacio(self):
        """Devuelve True si no hay elementos, y False en el caso contrario"""
        return not self._elementos

    def _intercambiar(self, i_a, i_b):
        self._elementos[i_a], self._elementos[i_b] = self._elementos[i_b], self._elementos[i_a]
    
    def _burbujeo_arriba(self, i):
        while i > 0:
            padre = (i - 1) // 2
            if self._elementos[padre] >= self._elementos[i]:
                break
            self._intercambiar(padre, i)
            i = padre

    def _burbujeo_abajo(self, i):
        n = len(self)
        while True:
            izq = 2 * i + 1
            der = 2 * i + 2
            mayor = i
            
            if izq < n and self._elementos[izq] > self._elementos[mayor]:
                mayor = izq
            if der < n and self._elementos[der] > self._elementos[mayor]:
                mayor = der
                
            if mayor == i:
                break
            self._intercambiar(i, mayor)
            i = mayor

    def insertar(self, valor):
        """Inserta un elemento nuevo y reordena el montículo"""
        self._elementos.append(valor)
        self._burbujeo_arriba(len(self) - 1)

    def consultar_maximo(self):
        """Devuelve el valor máximo en el montículo"""
        if self.esta_vacio():
            raise IndexError("El heap está vacío")
        return self._elementos[0]
    
    def extraer_maximo(self):
        """Devuelve el valor máximo en el montículo, quitándolo"""
        if self.esta_vacio():
            raise IndexError("El heap está vacío")
        
        maximo = self._elementos[0]
        ultimo = self._elementos.pop()

        if not self.esta_vacio():
            self._elementos[0] = ultimo
            self._burbujeo_abajo(0)

        return maximo

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