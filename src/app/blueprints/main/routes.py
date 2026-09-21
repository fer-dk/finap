# routes.py agrupa vistas (funciones de Python que devuelven respuestas HTTP).
from . import bp
from flask import render_template, abort
from app.config.navigation import main_sections

@bp.route("/", endpoint="home") # aqui se define
def home():
    return render_template("home.html", main_sections = main_sections)

# Prueba handlers
@bp.route("/test-500")
def test_500():
    raise Exception("error de prueba")