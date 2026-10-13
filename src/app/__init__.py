# Patrón utilizado - Application Factory / factory modular:
#   Permite registrar blueprints, tambien usar tests o configs por entorno
#   Evita importaciones circulares y Podés crear varias instancias de la app
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from pathlib import Path

# Las variables de .enc están "disponibles ANTES q python evalúe las clases de configuración"
from dotenv import load_dotenv
# Raíz del proyecto FINAP
BASE_DIR = Path(__file__).resolve().parent[2] # FINAP/ es parent[2], src/ es parent[1], app/ es parent[0]
load_dotenv(BASE_DIR / ".env")# Carga variables del archivo .env si existe

from app.config import DevConfig, ProdConfig, DevMigrationMysql

# --- Inicializamos Extensiones globales ---
db = SQLAlchemy()
migrate = Migrate()
# --- Models ---
from app.infrastructure import models # importa y registra las tablas
# --- Repos y port ---
from app.infrastructure.unit_of_work import Uowork
from app.infrastructure.log_repo import LogRepo
from app.infrastructure.prestacion_repo import PrestacionRepo
from app.infrastructure.user_repo import UserRepo
# --- Services ---
from app.application.log_service import LogService
from app.application.prestacion_service import PrestacionService
from app.application.auth_service import AuthService
from app.application.user_service import UserService

# Construye y devuelve una instancia de Flask configurada
def create_app():
    app = Flask(__name__, instance_relative_config=True) # Instancia de Flask
    env = os.environ.get("APP_ENV", "development") # seleccion configuración de Aplicación
    config_map = {"devlopment": DevConfig, "production": ProdConfig,}
    config_class = config_map.get(env) # Contiene una referencia a la propia clase

    # Validación 1: existe configuración?
    if config_class is None:
        raise ValueError(f"Configuracion desconocida en APP_ENV {env}")

    # Carga los atributos de la referencia de la clase configuración dentro de la aplicación
    app.config.from_object(config_class)

    # Validación 2 Dev/Prod:
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE URL es obligatoria para iniciar FINAP")
    # Validación 3 Prod:
    if env=="production" and not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY es obligatoria en producción")

    db.init_app(app) # conecta SQLAlchemy con Flask
    migrate.init_app(app, db) # conecta Flask-Migrate y registra comondo "db"

    # ADAPTADORES (definicion) === Inyeccion de dependencias ===
    app.log_repo = LogRepo(db)
    app.prestacion_repo = PrestacionRepo(db)
    app.uow_repo = Uowork(db)
    app.user_repo = UserRepo(db)

    # Servicios
    app.log_service = LogService(app.log_repo)
    app.prestacion_service = PrestacionService(app.prestacion_repo,app.log_repo, app.uow_repo)
    app.auth_service = AuthService(app.user_repo)
    app.user_service = UserService(app.user_repo, app.uow_repo)

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
    app.register_blueprint(auth_bp)

    from app.blueprints.users import bp as users_bp
    app.register_blueprint(users_bp)

    # Registrar Handlers
    # registramos la funcion que armamos en el handler directo sobre la factory
    from app.errors.handlers import register_error_handlers
    register_error_handlers(app)

    # === Context Processor inyecta menus a todas las plantillas ===
    from app.config.navigation import main_sections, navbars



    @app.context_processor
    def inject_navigation():
        bp_name = request.blueprint or "main"
        nav_items = navbars.get(bp_name)
        if nav_items is None:
            nav_items = navbars.get("main", [])
        return dict( #  retorna un diccionario con claves, inyectandolas al contexto jinja
            main_sections=main_sections,
            nav_items=nav_items,
            current_bp= bp_name
        )

    return app
