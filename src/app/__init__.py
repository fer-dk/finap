# Patrón utilizado - Application Factory / factory modular:
#   Permite registrar blueprints, tambien usar tests o configs por entorno
#   Evita importaciones circulares y Podés crear varias instancias de la app
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from app.config import DevMysql, DevLite, DevMigrationMysql

# --- Inicializamos Extensiones globales ---
db = SQLAlchemy()
migrate = Migrate()

# --- Modelos ---
from app.infrastructure import models # importa y registra las tablas
# --- Repos ---
from app.infrastructure.log_repo import LogRepo
from app.infrastructure.prestacion_repo import PrestacionRepo
from app.infrastructure.user_repo import UserRepo
# --- Servicios ---
from app.application.log_service import LogService
from app.application.prestacion_service import PrestacionService
from app.application.auth_service import AuthService

# Construye y devuelve una instancia de Flask configurada
def create_app():
    app = Flask(__name__, instance_relative_config=True) # Instancia de Flask

    env = os.environ.get("APP_ENV", "DevMysql") # Busca en el sistema APP_ENV

    config_map = {
        "DevMysql": DevMysql,
        "DevLite": DevLite,
        "DevMigrationMysql": DevMigrationMysql
    }

    config_class = config_map.get(env) # Bloque de seguridad
    if config_map is None:
        raise ValueError(
            f"Configuracion desconocida en APP_ENV {env}"
        )

    app.config.from_object(config_class) # Elige configuración

    db.init_app(app) # conecta SQLAlchemy con Flask
    migrate.init_app(app, db) # conecta Flask-Migrate y registra comondo "db"

    # ADAPTADORES (definicion) === Inyeccion de dependencias ===
    app.log_repo = LogRepo(db)
    app.prestacion_repo = PrestacionRepo(db)
    app.user_repo = UserRepo(db)

    # Servicios
    app.log_service = LogService(app.log_repo)
    app.prestacion_service = PrestacionService(app.prestacion_repo,app.log_repo, db)
    app.auth_service = AuthService(app.user_repo, db)

    # Registrar Blueprints
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix="")

    from app.blueprints.prestaciones import bp as prestaciones_bp
    app.register_blueprint(prestaciones_bp, url_prefix="")

    from app.blueprints.logs import bp as logs_bp
    app.register_blueprint(logs_bp, url_prefix="")

    from app.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="" )

    # === Context Processor inyecta menus a todas las plantillas ===
    from app.config.navigation import main_sections, navbars

    @app.context_processor # A
    def inject_navigation():
        bp_name = request.blueprint or "main" # aquí Flask reconoce de que blueprint viene la ruta actual (en que modulo está usuario). Es un atajo de un if pero no es un if
        nav_items = navbars.get(bp_name) # busca en el diccionario "navbar" de navigation.py al blueprint
        if nav_items is None:
            nav_items = navbars.get("main", [])
        return dict(
            main_sections=main_sections,
            nav_items=nav_items,
            current_bp= bp_name
        )

    return app

# A - # Context processor es una funcion especial que retorna un diccionario con claves,
      # esas claves las inyecta como variables globales al contexto de Jinja.
      # En vez de pasar manualmente las variables en cada render_template(),
      # automaticamente tiene acceso a ellas con contextprocessor.
      # Ventajas: No duplicamos includes ni pasamos manualmente listas desde cada controlador.
