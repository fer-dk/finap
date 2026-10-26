import os
from pathlib import Path
from datetime import timedelta

# ProductionConfig
# SECRET_KEY       → obligatoria
# cookie HttpOnly  → sí
# cookie Secure    → según HTTPS, normalmente sí
# SameSite         → política explícita
# duración sesión  → explícita

# Límite de Inactividad: 30m
# Límite absoluto: 8hrs

# Vigencia de "cookie" vs hrs autenticación "session"

# Politicas generales de sesión
class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # FLASK -------------------------------------------
    # controla la validez criptográfica y temporal.(configuración nativa de Flask)
    SESSION_COOKIE_HTTPONLY = True  # A
    SESSION_COOKIE_SAMESITE = "Lax" # B
    SESSION_REFRESH_EACH_REQUEST = False # C

    # 8 hrs de vigencia de cookie - CAMBIA
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8) # D

    # FINAP -------------------------------------------
    # Politica Combinada de Expiración de sesión. FINAP deberá comprobarlos en cada solicitud autenticada.

    SESSION_IDLE_TIMEOUT = timedelta(minutes=30) # E
    # 8 rhs del login autenticación - NO CAMBIA
    SESSION_ABSOLUTE_TIMEOUT = timedelta(hours=8) # F

# A - Impide que JavaScript acceda directamente a la cookie de sesión.

# B - Restringe el envío de cookies en solicitudes entre sitios.
#     Ayuda a reducir ciertos riesgos de CSRF.

# C - Evita que Flask renueve automáticamente la cookie permanente en cada respuesta.
#     No impide renovaciones por cambios de sesión. Aunque sea False genera una nueva cookie

# D - Flask utiliza es periodo para validar la antiguedad de firma de la cookie,
#     Si la app emite una nueva cookie de sesión durante la actividad, el plazo a asociado a la firma comienza nuevamente

# E - Tiempo máximo permitido desde la última actividad válida.
#     Cada actividad reconocida reinicia este contador.

# F - Conserva hora original. Si pasaron 8hrs, aunque considere valida la cookie rechazará la sesión

class DevConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret") # La sesión de Flask por defecto está firmada con SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SESSION_COOKIE_SECURE = False # Envia la cookie unicamente mediante HTTPS(adaptado a localhost)

# Representa las reglas de seguridad y comportamiento de una app en produccion
class ProdConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SESSION_COOKIE_SECURE = True # Presupone que el despliegue en producción utiliza HTTPS

class TestConfig(BaseConfig):
    TESTING = True # Nativo de Flask. Activa modo de pruebas
    SECRET_KEY = ("test-secret-key") # Clave solo para "testing". crea cookies firmadas durante las pruebas.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # Independiente de la db
    SESSION_COOKIE_SECURE = False # permite q el cliente de pruebas trabaje medianes HTTP sin necesitar HTTPS

class DevMigrationMysql():
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://finap_user:darliot2@127.0.0.1:3306/finap_migrations_tmp"
        "?charset=utf8mb4"
    )

# SECRET KEY
#   Clave secret de Flask para firmar cookies de sesion.
#   La firma protege la integridad, no la confidencialidad. Por eso no debemos guardar contraseñas ni información sensible en session.
#   Debe ser distintas en desarrollo y produccion. Se recomienda sacarla de una variable de entorno

# SQLALCHEMY_DATABASE_URI
#   Cadena de conexion (clave oficial) que Flask-SQLalchemy usa para conectarse a la base

# SQLALCHEMY_TRACK_MODIFICATIONS
#   Es propia de Flask-SQLalchemy. Controla si la extension debe seguir los cambios en los objetos para enviar señales
#   Usa False para evitar "overhead" y "warning" molestos

# UNC_PATH
# No es una palabra reservada, es una constante de configuracion para guardar la ruta UNC

# APP_ENV
#   No es una palabra reservada, Suele usarse para definir en que entorno estas, si development, production o testing