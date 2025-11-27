from db import init_db
from services.alquiler_service import crear_alquiler

def registrar_alquiler():
    print("\n=== REGISTRAR ALQUILER ===")

    fecha_recogida = input("Fecha de recogida (YYYY-MM-DD): ")
    fecha_devolucion = input("Fecha de devolución (YYYY-MM-DD): ")
    socio_id = int(input("ID del socio: "))

    # Pedimos múltiples películas separadas por comas
    peliculas_raw = input("IDs de películas (separados por coma): ")
    peliculas_ids = [int(pid.strip()) for pid in peliculas_raw.split(",")]

    alquiler_id = crear_alquiler(fecha_recogida, fecha_devolucion, socio_id, peliculas_ids)

    print(f"\n✔ Alquiler creado con ID: {alquiler_id}\n")


def main():
    init_db()

    while True:
        print("===== MENÚ VIDECLUB =====")
        print("1. Registrar socio")
        print("2. Registrar videoclub")
        print("3. Registrar película")
        print("4. Registrar alquiler")
        print("5. Calcular estadísticas")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "0":
            print("Saliendo...")
            break

        elif opcion == "4":
            registrar_alquiler()

        else:
            print(f"Opción elegida: {opcion} (función aún no implementada)\n")


if __name__ == "__main__":
    main()