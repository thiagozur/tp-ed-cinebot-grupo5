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
            print(f"{vertice} -> ", end="")
            vecinos = self.vertices[vertice]
            if vecinos:
                for vecino in vecinos:
                    print(f"{vecino} -> ", end="")
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

def dfs(grafo, origen, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(origen)
    resultado = [origen]
    for w in grafo[origen]:
        if w not in visitados:
            resultado += dfs(grafo, w, visitados)
    return resultado