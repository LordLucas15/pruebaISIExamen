from ..data import repositories as repo


def crear_socio(nombre: str, edad: int) -> int:
    return repo.create_socio(nombre, edad)


def listar_socios():
    return repo.list_socios()


