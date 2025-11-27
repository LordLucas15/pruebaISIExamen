class Videoclub:
    def __init__(self, gerente, ciudad, calle, codigo_postal, id=None):
        self.id = id
        self.gerente = gerente
        self.ciudad = ciudad
        self.calle = calle
        self.codigo_postal = codigo_postal