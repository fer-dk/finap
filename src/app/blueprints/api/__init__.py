from flask import Blueprint

# url_prefix , todas las rutas aca empiezan con /api
bp = Blueprint("api", __name__, url_prefix="/api")

from . import routes