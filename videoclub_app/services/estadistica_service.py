try:
    # Modo script: ejecutando desde videoclub_app (python main.py)
    from db import get_connection
except ImportError:  # pragma: no cover - fallback para modo paquete
    # Modo paquete: ejecutando como videoclub_app (python -m videoclub_app.app)
    from ..db import get_connection

from datetime import datetime


def calcular_total_por_socio_mes(anyo: int, mes: int):
    """
    Devuelve lista de dicts: {socio_id, nombre_socio, mes, total}
    anyo: int (e.g. 2025), mes: int (1..12)
    """
    mes_str = f"{anyo:04d}-{mes:02d}"
    conn = get_connection()
    cur = conn.cursor()

    # Relación alquiler -> alquiler_pelicula -> pelicula.precio
    cur.execute(
        """
    SELECT s.id, s.nombre, SUM(p.precio) as total
    FROM socio s
    JOIN alquiler a ON a.socio_id = s.id
    JOIN alquiler_pelicula ap ON ap.alquiler_id = a.id
    JOIN pelicula p ON p.id = ap.pelicula_id
    WHERE substr(a.fecha_recogida, 1, 7) = ?
    GROUP BY s.id, s.nombre
    """,
        (mes_str,),
    )
    rows = cur.fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append(
            {"socio_id": r[0], "nombre": r[1], "mes": mes_str, "total": r[2] or 0.0}
        )
    return result


def total_mes_por_socio(socio_id: int, mes_str: str) -> float:
    """
    Total gastado por un socio concreto en un mes (YYYY-MM).
    Usado por la parte web.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COALESCE(SUM(p.precio), 0.0) as total
        FROM alquiler a
        JOIN alquiler_pelicula ap ON ap.alquiler_id = a.id
        JOIN pelicula p ON p.id = ap.pelicula_id
        WHERE a.socio_id = ?
          AND substr(a.fecha_recogida, 1, 7) = ?
    """,
        (socio_id, mes_str),
    )
    row = cur.fetchone()
    conn.close()
    return float(row[0] or 0.0)


def calcular_total_mes(socio_id: int, mes_str: str) -> float:
    """
    Wrapper con el nombre que espera el CLI (`main.py`).
    """
    return total_mes_por_socio(socio_id, mes_str)


def guardar_estadistica(fecha_creacion, total, socio_id, mes_str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO estadistica (fecha_creacion, total, socio_id, mes)
        VALUES (?, ?, ?, ?)
    """,
        (fecha_creacion, total, socio_id, mes_str),
    )
    conn.commit()
    eid = cur.lastrowid
    conn.close()
    return eid
