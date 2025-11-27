from .db import get_connection
from typing import Iterable, Sequence


def create_socio(nombre: str, edad: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO socio (nombre, edad) VALUES (?, ?)", (nombre, edad))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def list_socios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, edad FROM socio ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def create_videoclub(gerente: str, ciudad: str, calle: str, codigo_postal: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO videoclub (gerente, ciudad, calle, codigo_postal) VALUES (?, ?, ?, ?)",
        (gerente, ciudad, calle, codigo_postal),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def list_videoclubs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, gerente, ciudad, calle, codigo_postal FROM videoclub ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def create_pelicula(nombre: str, director: str | None, fecha_estreno: str, precio: float, videoclub_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pelicula (nombre, director, fecha_estreno, precio, videoclub_id) VALUES (?, ?, ?, ?, ?)",
        (nombre, director, fecha_estreno, precio, videoclub_id),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def list_peliculas_with_videoclub():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.id, p.nombre, p.director, p.fecha_estreno, p.precio, v.ciudad AS videoclub_ciudad, v.gerente AS videoclub_gerente
        FROM pelicula p
        JOIN videoclub v ON v.id = p.videoclub_id
        ORDER BY p.id DESC
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def list_peliculas_simple():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM pelicula ORDER BY nombre ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def create_alquiler(fecha_recogida: str, fecha_devolucion: str, socio_id: int, peliculas_ids: Sequence[int]) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alquiler (fecha_recogida, fecha_devolucion, socio_id) VALUES (?, ?, ?)",
        (fecha_recogida, fecha_devolucion, socio_id),
    )
    alquiler_id = cur.lastrowid
    for pid in peliculas_ids:
        cur.execute(
            "INSERT INTO alquiler_pelicula (alquiler_id, pelicula_id) VALUES (?, ?)",
            (alquiler_id, pid),
        )
    conn.commit()
    conn.close()
    return alquiler_id


def total_mes_por_socio(socio_id: int, mes_prefix: str) -> float:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT SUM(p.precio) AS total
        FROM alquiler a
        JOIN alquiler_pelicula ap ON ap.alquiler_id = a.id
        JOIN pelicula p ON p.id = ap.pelicula_id
        WHERE a.socio_id = ?
          AND substr(a.fecha_recogida, 1, 7) = ?
        """,
        (socio_id, mes_prefix),
    )
    row = cur.fetchone()
    conn.close()
    return row["total"] if row and row["total"] is not None else 0.0


