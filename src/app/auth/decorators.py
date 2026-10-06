from functools import wraps
from flask import session, redirect, url_for, flash, request, abort

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs): # A
        if "user_id" not in session:
            if request.path.startswith("/api/"): # Vista API para devolver 401
                abort(401)
            flash("Debe iniciar sesión", "warning") # Vista Web para redirigir al login
            return redirect(url_for("auth.login_form", next=request.path))
        return view_func(*args, **kwargs)
    return wrapper


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if session.get("role") != required_role: # Tanto la vista API como WEB van al 403
                abort(403)
            return view_func(*args, **kwargs)
        return wrapper
    return decorator


# A - *args, **kwargs = - Permite que el decorator sea universal, funcionando con cualquier ruta.