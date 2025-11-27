from db import init_db

def main():
    init_db()   # crea la base de datos si no existe

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
        else:
            print(f"Opción elegida: {opcion} (función aún no implementada)\n")

if __name__ == "__main__":
    main()