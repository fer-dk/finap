import os
from pathlib import Path
from datetime import timedelta

from datetime import timedelta

# ProductionConfig
# SECRET_KEY       → obligatoria
# cookie HttpOnly  → sí
# cookie Secure    → según HTTPS, normalmente sí
# SameSite         → política explícita
# duración sesión  → explícita

# Límite de Inactividad: 30m
# Límite absoluto: 8hrs

# Politicas generales de sesión
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
    SESSION_IDLE_TIMEOUT = timedelta(minutes=30) # E
    SESSION_ABSOLUTE_TIMEOUT = timedelta(hours=8) # F

class DevConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret") # La sesión de Flask por defecto está firmada con SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get["DATABASE_URL"]
    SESSION_COOKIE_SECURE = False # Envia la cookie unicamente mediante HTTPS(adaptado a localhost)

# Representa las reglas de seguridad y comportamiento de una app en produccion
class ProdConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SESSION_COOKIE_SECURE = True # Presupone que el despliegue en producción utiliza HTTPS

# A - Impide que JavaScript acceda directamente a la cookie de sesión.

# B - Restringe el envío de cookies en solicitudes entre sitios.
#     Ayuda a reducir ciertos riesgos de CSRF.

# C - Evita que Flask renueve automáticamente la cookie permanente en cada respuesta.
#     No impide renovaciones por cambios de sesión.

# D - Controla vigencia de la cookie permanente (de sesión firmada), puede extenderse al emitir una nueva cookie.
#     Al vencer, Flask deja de aceptar la cookie vencida. FINAP rechazará la sesión pq pasaron 8hrs.
#     El rechazo se detecta sólo cuando llega una solicitud. No significa q cierre a las 8hrs

# E - Tiempo máximo permitido desde la última actividad válida.
#     Cada actividad reconocida reinicia este contador.

# F - FINAP detecta el vencimiento y rechaza la sesión
#     Tiempo máximo permitido desde el inicio de sesión original.
#     No se reinicia con la actividad ni con la renovación de cookies.




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

class DevMigrationMysql(DevMysql):
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://finap_user:darliot2@127.0.0.1:3306/finap_migrations_tmp"
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