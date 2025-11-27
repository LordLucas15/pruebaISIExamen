from db import get_connection
from models.alquiler import Alquiler

def crear_alquiler(fecha_recogida, fecha_devolucion, socio_id, peliculas_ids):
    conn = get_connection()
    cur = conn.cursor()

    # Crear fila en la tabla alquiler
    cur.execute("""
        INSERT INTO alquiler (fecha_recogida, fecha_devolucion, socio_id)
        VALUES (?, ?, ?)
    """, (fecha_recogida, fecha_devolucion, socio_id))

    alquiler_id = cur.lastrowid  # ID del alquiler recién creado

    # Registrar alquiler-película (relación N:M)
    for pelicula_id in peliculas_ids:
        cur.execute("""
            INSERT INTO alquiler_pelicula (alquiler_id, pelicula_id)
            VALUES (?, ?)
        """, (alquiler_id, pelicula_id))

    conn.commit()
    conn.close()

    return alquiler_id


def obtener_alquiler(alquiler_id):
    conn = get_connection()
    cur = conn.cursor()

    # Obtener datos del alquiler
    cur.execute("SELECT * FROM alquiler WHERE id = ?", (alquiler_id,))
    alquiler = cur.fetchone()

    if alquiler is None:
        conn.close()
        return None

    # Obtener películas asociadas
    cur.execute("""
        SELECT pelicula_id FROM alquiler_pelicula
        WHERE alquiler_id = ?
    """, (alquiler_id,))
    peliculas = [row[0] for row in cur.fetchall()]

    conn.close()

    return {
        "id": alquiler[0],
        "fecha_recogida": alquiler[1],
        "fecha_devolucion": alquiler[2],
        "socio_id": alquiler[3],
        "peliculas": peliculas
    }