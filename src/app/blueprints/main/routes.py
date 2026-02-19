# routes.py agrupa vistas (funciones de Python que devuelven respuestas HTTP).
from . import bp
from flask import render_template
from app.config.navigation import main_sections

@bp.route("/") # aqui se define
def home():
    return render_template("home.html", main_sections = main_sections)