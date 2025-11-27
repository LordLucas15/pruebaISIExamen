from ..data import repositories as repo


def total_mes_por_socio(socio_id: int, mes_prefix: str) -> float:
    return repo.total_mes_por_socio(socio_id, mes_prefix)


