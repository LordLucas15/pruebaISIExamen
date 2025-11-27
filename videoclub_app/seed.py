from services.videoclub_service import crear_videoclub
from services.socio_service import crear_socio
from services.pelicula_service import crear_pelicula
from services.alquiler_service import crear_alquiler
from db import init_db
from random import randint, choice
from datetime import datetime, timedelta

init_db()
print("Sembrando datos...")

# -----------------------------------------------------
# CREAR VIDECLUBS (10)
# -----------------------------------------------------
vc_data = [
    ("Ana Gómez", "Madrid", "Gran Via 23", "28013"),
    ("Carlos Ruiz", "Valencia", "Av. Puerto 99", "46021"),
    ("Lucía Martín", "Sevilla", "Sierpes 12", "41004"),
    ("Sergio Torres", "Barcelona", "Diagonal 240", "08018"),
    ("María Ríos", "Zaragoza", "Coso 102", "50001"),
    ("Jorge López", "Bilbao", "Moyúa 7", "48009"),
    ("Sandra Núñez", "Málaga", "Larios 3", "29005"),
    ("Pablo Prieto", "Murcia", "Mayor 15", "30003"),
    ("Elena Rivas", "Granada", "Reyes Católicos 44", "18002"),
    ("Ricardo Ortega", "Alicante", "Maisonnave 20", "03003"),
]

videoclubs = []
for gerente, ciudad, calle, cp in vc_data:
    videoclubs.append(crear_videoclub(gerente, ciudad, calle, cp))

print("Videoclubs creados:", videoclubs)

# -----------------------------------------------------
# CREAR SOCIOS (80)
# -----------------------------------------------------
nombre_base = [
    "Juan", "María", "Pedro", "Lucía", "Carlos", "Sofía", "Raúl", "Elena",
    "Miguel", "Laura", "Javier", "Ana", "Rubén", "Paula", "Héctor", "Lidia",
    "Sergio", "Alba", "Tomás", "Clara", "Iván", "Julia", "David", "Rosa",
    "Álvaro", "Carmen", "Adrián", "Marta", "Pablo", "Natalia", "Manuel",
    "Beatriz", "Diego", "Irene", "Mario", "Teresa", "Óscar", "Sara"
]

apellidos = [
    "Pérez", "García", "López", "Martín", "Fernández", "Sánchez", "Gómez",
    "Jiménez", "Ruiz", "Hernández", "Díaz", "Torres", "Suárez", "Ortega",
    "Moreno", "Vargas", "Castro", "Ramos", "Reyes", "Aguilar"
]

socios = []
for i in range(80):
    nombre = f"{choice(nombre_base)} {choice(apellidos)}"
    edad = randint(18, 70)
    socios.append(crear_socio(nombre, edad))

print("Socios creados:", len(socios))

# -----------------------------------------------------
# CREAR PELÍCULAS (120 películas realistas)
# -----------------------------------------------------

pelicula_catalogo = [
    ("Inception", "Christopher Nolan", "2010-07-16", 3.50),
    ("Interstellar", "Christopher Nolan", "2014-11-07", 3.80),
    ("Dunkirk", "Christopher Nolan", "2017-07-21", 3.20),
    ("Memento", "Christopher Nolan", "2000-09-05", 2.40),
    ("Avatar", "James Cameron", "2009-12-18", 3.20),
    ("Titanic", "James Cameron", "1997-12-19", 2.00),
    ("Terminator 2", "James Cameron", "1991-07-03", 2.20),
    ("Alien", "Ridley Scott", "1979-05-25", 2.40),
    ("Gladiator", "Ridley Scott", "2000-05-05", 2.70),
    ("Blade Runner", "Ridley Scott", "1982-06-25", 2.60),
    ("Matrix", "Wachowski", "1999-03-31", 2.50),
    ("Matrix Reloaded", "Wachowski", "2003-05-15", 2.80),
    ("Matrix Revolutions", "Wachowski", "2003-11-05", 2.80),
    ("Toy Story", "John Lasseter", "1995-11-22", 1.80),
    ("Toy Story 2", "John Lasseter", "1999-11-24", 2.10),
    ("Toy Story 3", "Lee Unkrich", "2010-06-18", 2.50),
    ("Shrek", "Andrew Adamson", "2001-05-18", 2.20),
    ("Shrek 2", "Andrew Adamson", "2004-05-19", 2.50),
    ("Shrek 3", "Chris Miller", "2007-05-06", 2.60),
    ("Cars", "John Lasseter", "2006-06-09", 1.90),
    ("Cars 2", "John Lasseter", "2011-06-24", 2.10),
    ("Cars 3", "Brian Fee", "2017-06-16", 2.20),
    ("Dune", "Denis Villeneuve", "2021-10-22", 3.40),
    ("Dune 2", "Denis Villeneuve", "2024-03-01", 4.20),
    ("Oppenheimer", "Christopher Nolan", "2023-07-21", 4.00),
    ("The Batman", "Matt Reeves", "2022-03-04", 3.90)
]

peliculas = []

# cada videoclub recibe copias de muchas películas
for vc in videoclubs:
    for titulo, director, estreno, precio in pelicula_catalogo:
        peliculas.append(crear_pelicula(titulo, director, estreno, precio, vc))

print("Películas creadas:", len(peliculas))

# -----------------------------------------------------
# CREAR ALQUILERES (150)
# -----------------------------------------------------
def random_date():
    # Todas las películas del catálogo se estrenan antes de 2024-03-01
    # así que alquilamos SOLO entre 2024 y 2025
    start = datetime(2024, 3, 2)  # justo después del estreno más reciente
    end = datetime(2025, 12, 31)

    # número de días entre start y end
    total_days = (end - start).days

    # escoger un día aleatorio
    random_days = randint(0, total_days)
    fecha_rec = start + timedelta(days=random_days)
    fecha_dev = fecha_rec + timedelta(days=randint(1, 7))

    return fecha_rec.strftime("%Y-%m-%d"), fecha_dev.strftime("%Y-%m-%d")

alquileres = []
for i in range(150):
    socio_id = choice(socios)
    fecha_rec, fecha_dev = random_date()
    peli1 = choice(peliculas)
    peli2 = choice(peliculas) if randint(0, 1) == 1 else None

    pelis = [peli1]
    if peli2:
        pelis.append(peli2)

    # validar que todas habían salido
    alquileres.append(crear_alquiler(fecha_rec, fecha_dev, socio_id, pelis))

print("Alquileres creados:", len(alquileres))
print("\n✔ Base de datos completamente rellenada.")
