from . import bp
from flask import render_template, current_app
from app.auth.decorators import login_required

@bp.route("/logs", methods=["GET"], endpoint="logs_list")
@login_required
def list_logs():
    service = current_app.log_service
    records = service.list()
    return render_template("logs/logs.html", records = records)