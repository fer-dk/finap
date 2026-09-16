from . import bp
from flask import render_template, current_app, request, redirect, flash,url_for
from app.auth.decorators import login_required, role_required

@bp.route("/users", methods=["GET"], endpoint="users_list")
@login_required
@role_required("admin")
def list_users():
    records=current_app.user_repo.list_users()
    return render_template("users/users_list.html", records=records)

@bp.route("/users/new", methods=["GET"], endpoint="user_form")
@login_required
@role_required("admin")
def user_form():
    return render_template("users/user_form.html")

@bp.route("/users", methods=["POST"], endpoint="user_create")
@login_required
@role_required("admin")
def create_user():
    username = request.form.get("username")
    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    role = request.form.get("role")

    try:
        current_app.user_service.register_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role
        )

        flash("Usuario creado correctamente", "success")
        return redirect(url_for("users.users_list"))

    except ValueError as e:
        flash(str(e), "warning")
        return redirect(url_for("users.user_form"))