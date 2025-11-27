try:
    # Modo script: ejecutando desde videoclub_app (python main.py)
    from db import get_connection
except ImportError:  # pragma: no cover - fallback para modo paquete
    # Modo paquete: ejecutando como videoclub_app (python -m videoclub_app.app)
    from ..db import get_connection

from datetime import datetime


def crear_alquiler(fecha_recogida, fecha_devolucion, socio_id, peliculas_ids):
    # -------------------------
    # VALIDACIÓN 1: Fechas
    # -------------------------
    if fecha_devolucion <= fecha_recogida:
        raise ValueError("La fecha de devolución debe ser posterior a la fecha de recogida.")

    # Convertir a fecha real para más seguridad
    try:
        fecha_rec = datetime.strptime(fecha_recogida, "%Y-%m-%d")
        fecha_dev = datetime.strptime(fecha_devolucion, "%Y-%m-%d")
    except Exception:
        raise ValueError("Formato incorrecto. Usa YYYY-MM-DD.")

    if fecha_dev <= fecha_rec:
        raise ValueError("La fecha de devolución debe ser posterior a la fecha de recogida.")

    conn = get_connection()
    cur = conn.cursor()

    # -------------------------
    # VALIDACIÓN 2: Película debe haber salido
    # -------------------------
    for pid in peliculas_ids:
        cur.execute("SELECT fecha_estreno FROM pelicula WHERE id = ?", (pid,))
        row = cur.fetchone()
        if row is None:
            conn.close()
            raise ValueError(f"La película con ID {pid} no existe.")

        fecha_estreno = datetime.strptime(row[0], "%Y-%m-%d")

        if fecha_estreno > fecha_rec:
            conn.close()
            raise ValueError(
                f"No puedes alquilar la película {pid} porque su estreno ({row[0]}) "
                f"es posterior a la fecha de recogida ({fecha_recogida})."
            )

    # -------------------------
    # INSERTAR ALQUILER
    # -------------------------
    cur.execute(
        """
        INSERT INTO alquiler (fecha_recogida, fecha_devolucion, socio_id)
        VALUES (?, ?, ?)
    """,
        (fecha_recogida, fecha_devolucion, socio_id),
    )

    alquiler_id = cur.lastrowid

    # -------------------------
    # INSERTAR RELACIÓN N:M
    # -------------------------
    for pid in peliculas_ids:
        cur.execute(
            """
            INSERT INTO alquiler_pelicula (alquiler_id, pelicula_id)
            VALUES (?, ?)
        """,
            (alquiler_id, pid),
        )

    conn.commit()
    conn.close()

    return alquiler_id


def obtener_alquiler(alquiler_id: int):
    """
    Devuelve un dict con la información básica del alquiler y
    los títulos de las películas asociadas, o None si no existe.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            a.id,
            a.fecha_recogida,
            a.fecha_devolucion,
            s.id AS socio_id,
            s.nombre AS socio_nombre,
            GROUP_CONCAT(p.nombre, ', ') AS peliculas
        FROM alquiler a
        JOIN socio s ON a.socio_id = s.id
        LEFT JOIN alquiler_pelicula ap ON ap.alquiler_id = a.id
        LEFT JOIN pelicula p ON p.id = ap.pelicula_id
        WHERE a.id = ?
        GROUP BY a.id, a.fecha_recogida, a.fecha_devolucion, s.id, s.nombre
    """,
        (alquiler_id,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "fecha_recogida": row[1],
        "fecha_devolucion": row[2],
        "socio_id": row[3],
        "socio_nombre": row[4],
        "peliculas": (row[5].split(", ") if row[5] else []),
    }