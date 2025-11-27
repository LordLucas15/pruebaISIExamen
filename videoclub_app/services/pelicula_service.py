from ..data import repositories as repo


def crear_pelicula(nombre: str, director: str | None, fecha_estreno: str, precio: float, videoclub_id: int) -> int:
    return repo.create_pelicula(nombre, director, fecha_estreno, precio, videoclub_id)


def listar_peliculas_con_videoclub():
    return repo.list_peliculas_with_videoclub()


def listar_peliculas_simple():
    return repo.list_peliculas_simple()


