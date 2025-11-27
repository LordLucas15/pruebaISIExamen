from db import get_connection

def crear_socio(nombre, edad):
    if edad < 0:
        raise ValueError("Edad no puede ser negativa.")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO socio (nombre, edad) VALUES (?, ?)", (nombre, edad))
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid

def obtener_socio(socio_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, edad FROM socio WHERE id = ?", (socio_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row[0], "nombre": row[1], "edad": row[2]}

def listar_socios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, edad FROM socio ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "edad": r[2]} for r in rows]
