import os
import sqlite3


def get_connection() -> sqlite3.Connection:
    # este archivo está en videoclub_app/data/db.py; la BD está en videoclub_app/videoclub.db
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "videoclub.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS videoclub (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gerente TEXT NOT NULL,
            ciudad TEXT NOT NULL,
            calle TEXT NOT NULL,
            codigo_postal TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS pelicula (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            director TEXT,
            fecha_estreno TEXT NOT NULL,
            precio REAL NOT NULL,
            videoclub_id INTEGER NOT NULL,
            FOREIGN KEY(videoclub_id) REFERENCES videoclub(id)
        );

        CREATE TABLE IF NOT EXISTS socio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS alquiler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_recogida TEXT NOT NULL,
            fecha_devolucion TEXT NOT NULL,
            socio_id INTEGER NOT NULL,
            FOREIGN KEY(socio_id) REFERENCES socio(id)
        );

        CREATE TABLE IF NOT EXISTS alquiler_pelicula (
            alquiler_id INTEGER,
            pelicula_id INTEGER,
            FOREIGN KEY(alquiler_id) REFERENCES alquiler(id),
            FOREIGN KEY(pelicula_id) REFERENCES pelicula(id)
        );

        CREATE TABLE IF NOT EXISTS estadistica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_creacion TEXT NOT NULL,
            total REAL NOT NULL,
            socio_id INTEGER NOT NULL,
            mes TEXT NOT NULL,
            FOREIGN KEY(socio_id) REFERENCES socio(id)
        );
        """
    )
    conn.commit()
    conn.close()


