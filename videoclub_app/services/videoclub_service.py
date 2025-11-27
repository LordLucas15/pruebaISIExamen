from db import get_connection

def crear_videoclub(gerente, ciudad, calle, codigo_postal):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO videoclub (gerente, ciudad, calle, codigo_postal)
        VALUES (?, ?, ?, ?)
    """, (gerente, ciudad, calle, codigo_postal))
    conn.commit()
    vid = cur.lastrowid
    conn.close()
    return vid

def obtener_videoclub(videoclub_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, gerente, ciudad, calle, codigo_postal FROM videoclub WHERE id = ?", (videoclub_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row[0], "gerente": row[1], "ciudad": row[2], "calle": row[3], "codigo_postal": row[4]}

def listar_videoclubs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, gerente, ciudad FROM videoclub ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "gerente": r[1], "ciudad": r[2]} for r in rows]
