class Pelicula:
    def __init__(self, id, titulo, director, genero, rating, anio):
        self._id = id
        self._titulo = titulo
        self._director = director
        self._genero = genero
        self._rating = rating
        self._anio = anio
        
    @property
    def titulo(self):
        return self._titulo

    @property
    def director(self):
        return self._director

    @property
    def genero(self):
        return self._genero

    @property
    def rating(self):
        return self._rating

    @property
    def anio(self):
        return self._anio

    def __repr__(self):
        return f"{self.titulo} ({self.anio}) - {self.genero} - {self.rating}/10 - Dirigida por {self.director}"