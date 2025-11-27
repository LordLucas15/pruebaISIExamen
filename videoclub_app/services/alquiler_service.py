from db import get_connection
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
    except:
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
    cur.execute("""
        INSERT INTO alquiler (fecha_recogida, fecha_devolucion, socio_id)
        VALUES (?, ?, ?)
    """, (fecha_recogida, fecha_devolucion, socio_id))

    alquiler_id = cur.lastrowid

    # -------------------------
    # INSERTAR RELACIÓN N:M
    # -------------------------
    for pid in peliculas_ids:
        cur.execute("""
            INSERT INTO alquiler_pelicula (alquiler_id, pelicula_id)
            VALUES (?, ?)
        """, (alquiler_id, pid))

    conn.commit()
    conn.close()

    return alquiler_id