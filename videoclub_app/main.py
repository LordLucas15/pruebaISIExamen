from db import init_db
from services.socio_service import crear_socio

def main():
    init_db()

    while True:
        print("1. Registrar socio")
        print("2. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            crear_socio(nombre, edad)
            print("Socio creado!")
        elif opcion == "2":
            break

if __name__ == "__main__":
    main()