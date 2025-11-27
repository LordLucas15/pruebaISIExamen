try:
    # Modo script: ejecutando dentro de videoclub_app (python main.py)
    from data.db import get_connection, init_db
except ImportError:  # pragma: no cover - fallback para modo paquete
    # Modo paquete: importando videoclub_app.db (python -m videoclub_app.app)
    from .data.db import get_connection, init_db

__all__ = ["get_connection", "init_db"]
