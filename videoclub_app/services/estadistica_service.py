from db import get_connection
from datetime import datetime

def calcular_total_por_socio_mes(anyo, mes):
    """
    Devuelve lista de dicts: {socio_id, nombre_socio, mes, total}
    anyo: int (e.g. 2025), mes: int (1..12)
    """
    mes_str = f"{anyo:04d}-{mes:02d}"
    conn = get_connection()
    cur = conn.cursor()

    # Suponemos: relacion alquiler -> alquiler_pelicula -> pelicula.precio
    cur.execute("""
    SELECT s.id, s.nombre, SUM(p.precio) as total
    FROM socio s
    JOIN alquiler a ON a.socio_id = s.id
    JOIN alquiler_pelicula ap ON ap.alquiler_id = a.id
    JOIN pelicula p ON p.id = ap.pelicula_id
    WHERE substr(a.fecha_recogida, 1, 7) = ?
    GROUP BY s.id, s.nombre
    """, (mes_str,))
    rows = cur.fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append({"socio_id": r[0], "nombre": r[1], "mes": mes_str, "total": r[2] or 0.0})
    return result

def guardar_estadistica(fecha_creacion, total, socio_id, mes_str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO estadistica (fecha_creacion, total, socio_id, mes)
        VALUES (?, ?, ?, ?)
    """, (fecha_creacion, total, socio_id, mes_str))
    conn.commit()
    eid = cur.lastrowid
    conn.close()
    return eid
