import os
from pathlib import Path

# Flask solo toma los atributos en MAYUSCULA del objeto/modulo
class DbConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

# Entorno Corporativo -----------------------------
class NasConfig(DbConfig):
    UNC_PATH = r"\\nasmoreno01\Finanzas 2\GESTION INFORMES DGF\DATOS\Rename\db3.sqlite"
    _sqlite_path = ("/////" + UNC_PATH.lstrip("\\").replace("\\", "/"))
    SQLALCHEMY_DATABASE_URI = f"sqlite:{_sqlite_path}?timeout=30"

class NasDevConfig(DbConfig):
    DEV_DB = Path(os.environ.get("LOCALAPPDATA", ".")) / "FINAP_DEV" / "db_dev.sqlite"
    DEV_DB.parent.mkdir(parents=True, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DEV_DB.as_posix()}"

# Entorno Backend Profesional ---------------------
class MacSqliteConfig(DbConfig):
    DEV_DB = Path.home() / "workspace" / "finap" / "data" / "db_dev.sqlite"
    DEV_DB.parent.mkdir(parents=True, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DEV_DB.as_posix()}"

class MacDevMySqlConfig(DbConfig):
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://finap_user:darliot2@127.0.0.1:3306/finap_dev"
        "?charset=utf8mb4"
        )


# SECRET KEY
#   Clave secret de Flask para firmar cookies de sesion
#   Protege formularios
#   Debe ser distintas en desarrollo y produccion
#   se recomienda sacarla de una variable de entorno

# SQLALCHEMY_DATABASE_URI
#   cadena de conexion que Flask-SQLalchemy usa para conectarse a la base
#   Esta si es una clave oficial de Flask-SQLalchemy

# SQLALCHEMY_TRACK_MODIFICATIONS
#   Es propia de Flask-SQLalchemy
#   Controla si la extension debe seguir los cambios en los objetos para enviar señales
#   Usa False para evitar "overhead" y "warning" molestos

# UNC_PATH
# No es una palabra reservada
# es una constante de configuracion para guardar la ruta UNC

# APP_ENV
#   No es una palabra reservada
#   Suele usarse para definir en que entorno estas, si development, production o testing

