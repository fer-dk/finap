# Patrón utilizado - Application Factory / factory modular:
#   Permite registrar blueprints, tambien usar tests o configs por entorno
#   Evita importaciones circulares
#   Podés crear varias instancias de la app

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from app.config import NasConfig, MacConfig

# --- Extensión global ---
db = SQLAlchemy()

# --- Importamos repo y servicios ---
from app.infrastructure.logs_repo import LogsRepo
from app.infrastructure.prestacion_repo import PrestacionRepo
from app.application.logs_service import LogsService
from app.application.prestacion_service import PrestacionService

# la siguiente funcion crea un objeto Flask
def create_app():
    # Instancia de Flask
    app = Flask(__name__, instance_relative_config=True)
    # Busca en el sistema una variable llamada APP_ENV
    env = os.environ.get("APP_ENV", "NasConfig")

    if env == "MacConfig":
        app.config.from_object(MacConfig)
    else:
        app.config.from_object(NasConfig)

    # app.config["EXPLAIN_TEMPLATE_LOADING"] = True

    db.init_app(app) # Inicializar extensión con la app

    # === Inyeccion de dependencias ===
    #Crear repos
    app.logs_repo = LogsRepo(db)
    app.prestacion_repo = PrestacionRepo(db)

    #Crear Servicios
    app.logs_service = LogsService(app.logs_repo)
    app.prestacion_service = PrestacionService(app.prestacion_repo,app.logs_repo)

    # === Registrar blueprints ===
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix="")

    from app.blueprints.prestaciones import bp as prestaciones_bp
    app.register_blueprint(prestaciones_bp, url_prefix="")

    from app.blueprints.logs import bp as logs_bp
    app.register_blueprint(logs_bp, url_prefix="")

    from app.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)



    # === Context Processor inyecta menus a todas las plantillas ===
    from app.config.navigation import main_sections, navbars

    # Context processor es una funcion especial que retorna un diccionario con claves,
    # esas claves las inyecta como variables globales al contexto de Jinja.
    # En vez de pasar manualmente las variables en cada render_template(),
    # automaticamente tiene acceso a ellas con contextprocessor.
    # Ventajas: No duplicamos includes ni pasamos manualmente listas desde cada controlador.

    @app.context_processor
    def inject_navigation():
        bp_name = request.blueprint or "main" # aquí Flask reconoce de que blueprint viene la ruta actual (en que modulo está usuario). Es un atajo de un if pero no es un if
        nav_items = navbars.get(bp_name) # busca en el diccionario "navbar" de navigation.py al blueprint
        if nav_items is None:
            nav_items = navbars.get("main", [])
        return dict(
            main_sections=main_sections, # "main_sections": main_sections - resultado "Prestaciones"
            nav_items=nav_items,    # resultado "Listar"
            current_bp= bp_name     # resultado "prestaciones"
        )

    return app