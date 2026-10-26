import os
from pathlib import Path
from datetime import timedelta

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Seguridad de cookies (configuración nativa de Flask)
    # Flask controla la validez criptográfica y temporal de la cookie.
    SESSION_COOKIE_HTTPONLY = True  # A
    SESSION_COOKIE_SAMESITE = "Lax" # B
    SESSION_REFRESH_EACH_REQUEST = False # C
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8) # D

    # Política FINAP (configuración No nativas) FINAP controla la política de atenticación del Usuario
    # Flask no aplica estos límites automáticamente. FINAP deberá comprobarlos en cada solicitud autenticada.
    SESSION_IDLE_TIMEOUT = timedelta(minutes=2) # E
    SESSION_ABSOLUTE_TIMEOUT = timedelta(minutes=5) # F


# Entorno Corporativo -----------------------------
class Nas(BaseConfig):
    UNC_PATH = r"\\nasmoreno01\Finanzas 2\GESTION INFORMES DGF\DATOS\Rename\db3.sqlite"
    _sqlite_path = ("/////" + UNC_PATH.lstrip("\\").replace("\\", "/"))
    SQLALCHEMY_DATABASE_URI = f"sqlite:{_sqlite_path}?timeout=30"

class NasDev(BaseConfig):
    DEV_DB = Path(os.environ.get("LOCALAPPDATA", ".")) / "FINAP_DEV" / "db_dev.sqlite"
    DEV_DB.parent.mkdir(parents=True, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DEV_DB.as_posix()}"

# Entorno Backend Profesional ---------------------
class DevLite(BaseConfig):
    DEV_DB = Path.home() / "workspace" / "finap" / "data" / "db_dev.sqlite"
    DEV_DB.parent.mkdir(parents=True, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DEV_DB.as_posix()}"

class DevMysql(BaseConfig):
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://finap_user:darliot2@127.0.0.1:3306/finap_dev"
        "?charset=utf8mb4"
        )

