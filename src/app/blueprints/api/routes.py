from . import bp
from flask import jsonify

@bp.route("/ping", methods=["GET"])
def ping():
    # respuesta JSN de verificacion
    return jsonify({"status": "ok", "message": "API viva"})
