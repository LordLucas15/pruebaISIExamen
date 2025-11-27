from ..data import repositories as repo


def crear_videoclub(gerente: str, ciudad: str, calle: str, codigo_postal: str) -> int:
    return repo.create_videoclub(gerente, ciudad, calle, codigo_postal)


def listar_videoclubs():
    return repo.list_videoclubs()


