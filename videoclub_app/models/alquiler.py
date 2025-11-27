class Alquiler:
    def __init__(self, fecha_recogida, fecha_devolucion, socio_id, peliculas_ids):
        self.fecha_recogida = fecha_recogida
        self.fecha_devolucion = fecha_devolucion
        self.socio_id = socio_id
        self.peliculas_ids = peliculas_ids  # lista de IDs de películas