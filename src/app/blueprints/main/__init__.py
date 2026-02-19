from flask import Blueprint

# Instancia de Blueprint
bp = Blueprint("main", __name__) # al no tener un template propio, de esta forma (sin paramentro de "template_folder") llama al template Global

# Ejecuta las vistas decoradas, para que queden registradas en bp
# Esas vistas están asociadas a rutas URL mediante los decoradores @bp.route("/...").
from . import routes




