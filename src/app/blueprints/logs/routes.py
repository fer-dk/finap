from . import bp
from flask import render_template, current_app

@bp.route("/logs", methods=["GET"], endpoint="logs_list")
def list_logs():
    service = current_app.log_service
    records = service.list()
    return render_template("logs/logs.html", records = records)