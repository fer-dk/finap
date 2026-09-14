from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs): # A
        if "user_id" not in session:
            flash("Debe iniciar sesión", "warning")
            return redirect(url_for("auth.login_form", next=request.path))
        return view_func(*args, **kwargs)
    return wrapper


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if session.get("role") != required_role:
                flash("No tiene permisos para acceder a esta sección.", "warning")
                return redirect(url_for("main.home"))
            return view_func(*args, **kwargs)
        return wrapper
    return decorator


# A - *args, **kwargs = - Permite que el decorator sea universal, funcionando con cualquier ruta.