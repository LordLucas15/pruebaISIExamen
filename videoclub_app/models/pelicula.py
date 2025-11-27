class Pelicula:
    def __init__(self, nombre, director, fecha_estreno, precio, videoclub_id, id=None):
        self.id = id
        self.nombre = nombre
        self.director = director
        self.fecha_estreno = fecha_estreno
        self.precio = precio
        self.videoclub_id = videoclub_id
