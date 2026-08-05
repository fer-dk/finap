from . import bp
from flask import render_template, request, redirect, url_for, flash, session, current_app
from app.config.navigation import main_sections

@bp.route("/login", methods=["GET"], endpoint="login_form")
def login_form():
    return render_template("auth/login.html")

@bp.route("/login", methods=["POST"], endpoint="login_post")
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        user = current_app.auth_service.login(username, password)
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        flash("Inicio de sesión correcta.", "login")
        next_url = request.form.get("next") # Recuperamos el "next" que viene del decorador

        if next_url:
            return redirect(next_url)

        return redirect(url_for("main.home"))

    except ValueError as e:
        # print("login error", e)
        flash(str(e), "login-error")
        return redirect(url_for("auth.login_form"))

@bp.route("/logout", methods=["GET"], endpoint="logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("auth.login_form"))

