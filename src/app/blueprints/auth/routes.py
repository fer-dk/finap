from . import bp
from flask import  render_template, request, redirect, url_for, flash, session, current_app
from app.config.navigation import main_sections
from datetime import datetime, timezone

@bp.route("/login", methods=["GET"], endpoint="login_form")
def login_form():
    return render_template("auth/login.html")

@bp.route("/login", methods=["POST"], endpoint="login_post")
def login_post():
    username=request.form.get("username")
    password=request.form.get("password")

    try:
        # Autenticación
        user=current_app.auth_service.login(username, password)

        # Inicio de nueva sesión permanente
        session.clear() # Limpia datos del objeto sesiónantes antes de establecer la nueva identidad
        session.permanent = True # Flask utiliza esta caracteristica del objeto de sesión para en BaseConfig determinar la duración

        # Registro (fijo) del instante inicial de autenticación
        now = datetime.now(timezone.utc).timestamp()

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        session["login_at"] = now # referencia absoluta de autenticación
        session["last_activity"] = now # calcula el limite de inactividad

        flash("Inicio de sesión correcta", "success")
        next_url = request.form.get("next") # recuperamos el next que viene del decorador

        if next_url:
            return redirect(next_url)

        return redirect(url_for("main.home"))

    except ValueError as e:
        flash(str(e), "login-error")
        return redirect(url_for("auth.login_form"))

@bp.route("/logout", methods=["GET"], endpoint="logout")
def logout():
    session.clear()
    flash("Sesión cerrada con éxito", "info")
    return redirect(url_for("auth.login_form"))