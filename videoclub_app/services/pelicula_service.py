try:
    # Modo script: ejecutando desde videoclub_app (python main.py)
    from db import get_connection
except ImportError:  # pragma: no cover - fallback para modo paquete
    # Modo paquete: ejecutando como videoclub_app (python -m videoclub_app.app)
    from ..db import get_connection


def crear_pelicula(nombre, director, fecha_estreno, precio, videoclub_id):
    conn = get_connection()
    cur = conn.cursor()
    # comprobar que videoclub existe
    cur.execute("SELECT id FROM videoclub WHERE id = ?", (videoclub_id,))
    if cur.fetchone() is None:
        conn.close()
        raise ValueError("El videoclub indicado no existe.")
    cur.execute(
        """
        INSERT INTO pelicula (nombre, director, fecha_estreno, precio, videoclub_id)
        VALUES (?, ?, ?, ?, ?)
    """,
        (nombre, director, fecha_estreno, precio, videoclub_id),
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def obtener_pelicula(pelicula_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nombre, director, fecha_estreno, precio, videoclub_id FROM pelicula WHERE id = ?",
        (pelicula_id,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "nombre": row[1],
        "director": row[2],
        "fecha_estreno": row[3],
        "precio": row[4],
        "videoclub_id": row[5],
    }


def listar_peliculas(videoclub_id=None):
    conn = get_connection()
    cur = conn.cursor()
    if videoclub_id:
        cur.execute(
            "SELECT id, nombre, precio FROM pelicula WHERE videoclub_id = ? ORDER BY id",
            (videoclub_id,),
        )
    else:
        cur.execute("SELECT id, nombre, precio FROM pelicula ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "precio": r[2]} for r in rows]


def listar_peliculas_simple():
    """Devuelve películas mínimas para selects (id, nombre)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM pelicula ORDER BY nombre")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "nombre": r[1]} for r in rows]


def listar_peliculas_con_videoclub():
    """Listado detallado para la pantalla de películas con ciudad del videoclub."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.id, p.nombre, p.director, p.fecha_estreno, p.precio, v.ciudad
        FROM pelicula p
        JOIN videoclub v ON p.videoclub_id = v.id
        ORDER BY p.id
    """
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "nombre": r[1],
            "director": r[2],
            "fecha_estreno": r[3],
            "precio": r[4],
            "videoclub_ciudad": r[5],
        }
        for r in rows
    ]
