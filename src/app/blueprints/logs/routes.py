from . import bp
from flask import render_template, current_app

@bp.route("/logs", methods=["GET"], endpoint="logs_listar")
def listar_logs():
    service = current_app.log_service
    registros = service.listar()
    return render_template("logs/logs.html", registros = registros)