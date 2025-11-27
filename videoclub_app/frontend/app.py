from flask import Flask, render_template, request, redirect, url_for, flash
from ..data.db import init_db
from ..services import socio_service, videoclub_service, pelicula_service, alquiler_service, estadistica_service
import os


def create_app() -> Flask:
    here = os.path.dirname(__file__)
    app = Flask(__name__, template_folder=os.path.join(here, "templates"), static_folder=os.path.join(here, "static"))
    app.config["SECRET_KEY"] = "dev-secret"

    with app.app_context():
        init_db()

    @app.get("/")
    def index():
        return render_template("home.html")

    @app.route("/socios", methods=["GET", "POST"])
    def socios():
        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            edad = request.form.get("edad", "").strip()
            if not nombre or not edad.isdigit():
                flash("Nombre y edad válidos son obligatorios.", "error")
            else:
                socio_service.crear_socio(nombre, int(edad))
                flash("Socio creado correctamente.", "success")
            return redirect(url_for("socios"))
        q = request.args.get("q", "").strip()
        page_raw = request.args.get("page", "1")
        try:
            page = max(1, int(page_raw))
        except ValueError:
            page = 1

        socios_list = socio_service.listar_socios()
        if q:
            q_lower = q.lower()
            socios_list = [
                s
                for s in socios_list
                if q_lower in str(s["id"]).lower()
                or q_lower in s["nombre"].lower()
            ]

        page_size = 50
        total = len(socios_list)
        start = (page - 1) * page_size
        end = start + page_size
        socios_page = socios_list[start:end]
        total_pages = max(1, (total + page_size - 1) // page_size) if total else 1

        return render_template(
            "socios.html",
            socios=socios_page,
            q=q,
            page=page,
            total_pages=total_pages,
        )

    @app.route("/videoclubs", methods=["GET", "POST"])
    def videoclubs():
        if request.method == "POST":
            gerente = request.form.get("gerente", "").strip()
            ciudad = request.form.get("ciudad", "").strip()
            calle = request.form.get("calle", "").strip()
            codigo_postal = request.form.get("codigo_postal", "").strip()
            if not (gerente and ciudad and calle and codigo_postal):
                flash("Todos los campos son obligatorios.", "error")
            else:
                videoclub_service.crear_videoclub(gerente, ciudad, calle, codigo_postal)
                flash("Videoclub creado correctamente.", "success")
            return redirect(url_for("videoclubs"))
        q = request.args.get("q", "").strip()
        page_raw = request.args.get("page", "1")
        try:
            page = max(1, int(page_raw))
        except ValueError:
            page = 1

        lista = videoclub_service.listar_videoclubs()
        if q:
            q_lower = q.lower()
            lista = [
                v
                for v in lista
                if q_lower in str(v["id"]).lower()
                or q_lower in v["gerente"].lower()
                or q_lower in v["ciudad"].lower()
            ]

        page_size = 50
        total = len(lista)
        start = (page - 1) * page_size
        end = start + page_size
        videoclubs_page = lista[start:end]
        total_pages = max(1, (total + page_size - 1) // page_size) if total else 1

        return render_template(
            "videoclubs.html",
            videoclubs=videoclubs_page,
            q=q,
            page=page,
            total_pages=total_pages,
        )

    @app.route("/peliculas", methods=["GET", "POST"])
    def peliculas():
        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            director = request.form.get("director", "").strip() or None
            fecha_estreno = request.form.get("fecha_estreno", "").strip()
            precio = request.form.get("precio", "").strip()
            videoclub_id = request.form.get("videoclub_id", "").strip()
            if not (nombre and fecha_estreno and precio and videoclub_id.isdigit()):
                flash("Campos requeridos inválidos.", "error")
            else:
                try:
                    pelicula_service.crear_pelicula(nombre, director, fecha_estreno, float(precio), int(videoclub_id))
                    flash("Película creada correctamente.", "success")
                except Exception as ex:
                    flash(f"Error al crear película: {ex}", "error")
            return redirect(url_for("peliculas"))
        q = request.args.get("q", "").strip()
        page_raw = request.args.get("page", "1")
        try:
            page = max(1, int(page_raw))
        except ValueError:
            page = 1

        videoclubs = videoclub_service.listar_videoclubs()
        peliculas_list = pelicula_service.listar_peliculas_con_videoclub()
        if q:
            q_lower = q.lower()
            peliculas_list = [
                p
                for p in peliculas_list
                if q_lower in str(p["id"]).lower()
                or q_lower in p["nombre"].lower()
                or (p["director"] and q_lower in p["director"].lower())
                or q_lower in p["videoclub_ciudad"].lower()
            ]

        page_size = 50
        total = len(peliculas_list)
        start = (page - 1) * page_size
        end = start + page_size
        peliculas_page = peliculas_list[start:end]
        total_pages = max(1, (total + page_size - 1) // page_size) if total else 1

        return render_template(
            "peliculas.html",
            peliculas=peliculas_page,
            videoclubs=videoclubs,
            q=q,
            page=page,
            total_pages=total_pages,
        )

    @app.route("/alquileres/nuevo", methods=["GET", "POST"])
    def alquiler_nuevo():
        if request.method == "POST":
            fecha_recogida = request.form.get("fecha_recogida", "").strip()
            fecha_devolucion = request.form.get("fecha_devolucion", "").strip()
            socio_id = request.form.get("socio_id", "").strip()
            peliculas_ids = request.form.getlist("peliculas_ids")
            peliculas_ids_int = [int(pid) for pid in peliculas_ids if pid.isdigit()]
            if not (fecha_recogida and fecha_devolucion and socio_id.isdigit() and peliculas_ids_int):
                flash("Todos los campos son obligatorios.", "error")
            else:
                alquiler_id = alquiler_service.crear_alquiler(fecha_recogida, fecha_devolucion, int(socio_id), peliculas_ids_int)
                flash(f"Alquiler creado con ID {alquiler_id}.", "success")
                return redirect(url_for("alquiler_nuevo"))
        socios_list = socio_service.listar_socios()
        peliculas_list = pelicula_service.listar_peliculas_simple()

        q = request.args.get("q", "").strip()
        page_raw = request.args.get("page", "1")
        try:
            page = max(1, int(page_raw))
        except ValueError:
            page = 1

        alquileres_list = alquiler_service.listar_alquileres()
        if q:
            q_lower = q.lower()
            alquileres_list = [
                a
                for a in alquileres_list
                if q_lower in str(a["id"]).lower()
                or q_lower in a["socio_nombre"].lower()
            ]

        page_size = 50
        total = len(alquileres_list)
        start = (page - 1) * page_size
        end = start + page_size
        alquileres_page = alquileres_list[start:end]
        total_pages = max(1, (total + page_size - 1) // page_size) if total else 1

        return render_template(
            "alquiler_nuevo.html",
            socios=socios_list,
            peliculas=peliculas_list,
            alquileres=alquileres_page,
            q=q,
            page=page,
            total_pages=total_pages,
        )

    @app.route("/estadisticas", methods=["GET", "POST"])
    def estadisticas():
        total = None
        socio_sel = None
        mes_sel = None
        socios_list = socio_service.listar_socios()
        if request.method == "POST":
            socio_sel = request.form.get("socio_id", "").strip()
            mes_sel = request.form.get("mes", "").strip()
            if socio_sel.isdigit() and mes_sel:
                total = estadistica_service.total_mes_por_socio(int(socio_sel), mes_sel)
            else:
                flash("Selecciona un socio y un mes válido (YYYY-MM).", "error")
        return render_template("estadisticas.html", socios=socios_list, total=total, socio_sel=socio_sel, mes_sel=mes_sel)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


