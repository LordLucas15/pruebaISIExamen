from db import init_db
from services.socio_service import crear_socio, listar_socios
from services.videoclub_service import crear_videoclub, listar_videoclubs
from services.pelicula_service import crear_pelicula, listar_peliculas
from services.alquiler_service import crear_alquiler, obtener_alquiler
from services.estadistica_service import calcular_total_por_socio_mes, guardar_estadistica
from datetime import datetime
from services.estadistica_service import calcular_total_mes, guardar_estadistica


def input_int(prompt):
    val = input(prompt)
    try:
        return int(val)
    except:
        return None

def registrar_socio():
    print("\n=== REGISTRAR SOCIO ===")
    nombre = input("Nombre: ").strip()
    edad = input_int("Edad: ")
    if edad is None:
        print("Edad inválida.")
        return
    sid = crear_socio(nombre, edad)
    print(f"Socio creado con ID: {sid}\n")

def registrar_videoclub():
    print("\n=== REGISTRAR VIDEOCLUB ===")
    gerente = input("Gerente: ").strip()
    ciudad = input("Ciudad: ").strip()
    calle = input("Calle: ").strip()
    cp = input("Código postal: ").strip()
    vid = crear_videoclub(gerente, ciudad, calle, cp)
    print(f"Videoclub creado con ID: {vid}\n")

def registrar_pelicula():
    print("\n=== REGISTRAR PELÍCULA ===")
    nombre = input("Nombre: ").strip()
    director = input("Director: ").strip()
    fecha = input("Fecha estreno (YYYY-MM-DD): ").strip()
    precio_raw = input("Precio: ").strip()
    try:
        precio = float(precio_raw)
    except:
        print("Precio inválido.")
        return
    # listar videoclubs para seleccionar
    vds = listar_videoclubs()
    if not vds:
        print("No hay videoclubs. Crea uno antes.")
        return
    print("Videoclubs disponibles:")
    for v in vds:
        print(f"{v['id']}: {v['gerente']} ({v['ciudad']})")
    videoclub_id = input_int("ID videoclub: ")
    if videoclub_id is None:
        print("ID inválido.")
        return
    try:
        pid = crear_pelicula(nombre, director, fecha, precio, videoclub_id)
        print(f"Película creada con ID: {pid}\n")
    except Exception as e:
        print("Error:", e)

def registrar_alquiler_menu():
    print("\n=== REGISTRAR ALQUILER ===")
    # listar socios
    socios = listar_socios()
    if not socios:
        print("No hay socios registrados. Crea uno primero.")
        return
    print("Socios:")
    for s in socios:
        print(f"{s['id']}: {s['nombre']} ({s['edad']} años)")

    socio_id = input_int("ID del socio: ")
    if socio_id is None:
        print("ID inválido.")
        return

    # listar peliculas
    peliculas = listar_peliculas()
    if not peliculas:
        print("No hay películas registradas.")
        return
    print("Películas:")
    for p in peliculas:
        print(f"{p['id']}: {p['nombre']} (precio: {p['precio']})")

    peliculas_raw = input("IDs de películas (separados por coma): ").strip()
    try:
        peliculas_ids = [int(x.strip()) for x in peliculas_raw.split(",") if x.strip()]
    except:
        print("IDs inválidos.")
        return

    fecha_recogida = input("Fecha recogida (YYYY-MM-DD): ").strip()
    fecha_devolucion = input("Fecha devolución (YYYY-MM-DD): ").strip()

    alquiler_id = crear_alquiler(fecha_recogida, fecha_devolucion, socio_id, peliculas_ids)
    print(f"Alquiler creado con ID: {alquiler_id}\n")

def ver_alquiler():
    aid = input_int("Introduce ID de alquiler para ver: ")
    if aid is None:
        print("ID inválido.")
        return
    data = obtener_alquiler(aid)
    if not data:
        print("Alquiler no encontrado.")
        return
    print("Alquiler:", data)

def calcular_estadisticas_menu():
    print("\n=== CALCULAR ESTADÍSTICA ===")

    socio_id = int(input("ID del socio: "))
    año = input("Año (YYYY): ")
    mes = input("Mes (MM): ")

    mes_str = f"{año}-{mes}"

    total = calcular_total_mes(socio_id, mes_str)

    print(f"Total gastado por socio {socio_id} en {mes_str}: {total}€")

    fecha_creacion = input("Introduce fecha de creación estadística (YYYY-MM-DD): ")

    try:
        guardar_estadistica(fecha_creacion, total, socio_id, mes_str)
        print("✔ Estadística guardada correctamente\n")
    except ValueError as e:
        print("Error:", e)


def main():
    init_db()
    while True:
        print("===== MENÚ VIDECLUB =====")
        print("1. Registrar socio")
        print("2. Registrar videoclub")
        print("3. Registrar película")
        print("4. Registrar alquiler")
        print("6. Ver alquiler (por ID)")
        print("5. Calcular estadísticas")
        print("0. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "0":
            print("Saliendo...")
            break
        elif opcion == "1":
            registrar_socio()
        elif opcion == "2":
            registrar_videoclub()
        elif opcion == "3":
            registrar_pelicula()
        elif opcion == "4":
            registrar_alquiler_menu()
        elif opcion == "6":
            ver_alquiler()
        elif opcion == "5":
            calcular_estadisticas_menu()
        else:
            print("Opción no válida.\n")

if __name__ == "__main__":
    main()
