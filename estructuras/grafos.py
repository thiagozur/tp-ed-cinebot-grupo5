from estructuras.heaps import MinHeap

class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, valor):
        if valor not in self.vertices:
            self.vertices[valor] = []

    def agregar_arista(self, v_desde, v_hasta):
        if v_desde in self.vertices and v_hasta in self.vertices:
            if v_hasta not in self.vertices[v_desde]:
                self.vertices[v_desde].append(v_hasta)
            if v_desde not in self.vertices[v_hasta]:
                self.vertices[v_hasta].append(v_desde)
        else:
            raise ValueError("Vértice inválido")

    def mostrar(self):
        for vertice in self.vertices:
            print(f"{vertice} -> ", end = "")
            vecinos = self.vertices[vertice]
            if vecinos:
                for vecino in vecinos:
                    print(f"{vecino} -> ", end = "")
            print("None")

class Digrafo: 
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, valor):
        if valor not in self.vertices:
            self.vertices[valor] = []

    def agregar_arista(self, v_desde, v_hasta):
        if v_desde in self.vertices and v_hasta in self.vertices:
            if v_hasta not in self.vertices[v_desde]:
                self.vertices[v_desde].append(v_hasta)
        else:
            raise ValueError("Vértice inválido")

    def mostrar(self):
        for vertice in self.vertices:
            print(f"{vertice} -> ", end = "")
            vecinos = self.vertices[vertice]
            if vecinos:
                for vecino in vecinos:
                    print(f"{vecino} -> ", end = "")
            print("None")

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

def bfs(grafo, origen):
    visitados = {origen}
    cola = [origen]
    orden = []
    while cola:
        v = cola.pop(0)
        orden.append(v)
        for w in grafo[v]:
            if w not in visitados:
                visitados.add(w)
                cola.append(w)
    return orden

def dfs(grafo, origen, visitados = None):
    if visitados is None:
        visitados = set()
    visitados.add(origen)
    resultado = [origen]
    for w in grafo[origen]:
        if w not in visitados:
            resultado += dfs(grafo, w, visitados)
    return resultado

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

def dijkstra(grafo, origen, destino):
    distancias = {v: float("inf") for v in grafo}
    predecesores = {v: None for v in grafo}
    distancias[origen] = 0.0

    heap = MinHeap()
    contador = 0
    heap.insertar((0.0, contador, origen))

    while not heap.esta_vacio():
        costo_actual, _, actual = heap.extraer_minimo()

        if actual == destino:
            break
        if costo_actual > distancias[actual]:
            continue

        for vecino, peso in grafo[actual].items():
            nuevo_costo = costo_actual + peso
            if nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                predecesores[vecino] = actual
                contador += 1
                heap.insertar((nuevo_costo, contador, vecino))

    if distancias[destino] == float("inf"):
        return [], float("inf")

    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = predecesores[actual]
    camino.reverse()
    return camino, round(distancias[destino], 2)