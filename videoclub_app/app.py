# Mantener archivo por compatibilidad: redirige a la nueva app en frontend
from .frontend.app import create_app  # noqa: E402,F401



if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
