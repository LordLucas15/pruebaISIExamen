from ..data import repositories as repo
from typing import Sequence


def crear_alquiler(fecha_recogida: str, fecha_devolucion: str, socio_id: int, peliculas_ids: Sequence[int]) -> int:
    return repo.create_alquiler(fecha_recogida, fecha_devolucion, socio_id, peliculas_ids)


def obtener_alquiler(alquiler_id: int):
    # consulta simplificada para mantener paridad con la versión previa
    from ..data.db import get_connection

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alquiler WHERE id = ?", (alquiler_id,))
    alquiler = cur.fetchone()
    if alquiler is None:
        conn.close()
        return None
    cur.execute("SELECT pelicula_id FROM alquiler_pelicula WHERE alquiler_id = ?", (alquiler_id,))
    peliculas = [row[0] for row in cur.fetchall()]
    conn.close()
    return {
        "id": alquiler[0],
        "fecha_recogida": alquiler[1],
        "fecha_devolucion": alquiler[2],
        "socio_id": alquiler[3],
        "peliculas": peliculas,
    }