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

# A - *args, **kwargs = - Permite que el decorator sea universal, funcionando con cualquier ruta.