#CONTROLLERS
from . import bp
from app.auth.decorators import login_required, role_required
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app

# Controlador HTTP / HTML (capa de interfaz)
@bp.route("/prestacion", methods=["GET"], endpoint="prestacion_form") #B,C
@login_required # A - Adaptador de Entrada (Controller/Driver) de seguridad (no es capa de seguridad)
@role_required("admin")
def show_form(): # View Fuction
    # Actua como un Presenter
    return render_template("prestaciones/prestacion.html")

@bp.route("/prestacion", methods=["POST"], endpoint="prestacion_insert")
def insert_prestacion():
    # Aqui estas en la capa http: lee datos de la request
    namePres = (request.form.get("namePrestacion") or "").strip()
    if not namePres:
        flash("Debe ingresar un nombre", "warning")
        return redirect(url_for("prestaciones.prestacion_form"))

    # Adaptador HTTP: llama al caso de uso y pasa los objetos de dominio a la vista
    service = current_app.prestacion_service
    service.create(namePres)
    flash("Registro y Log con éxito", "success")
    return redirect(url_for("prestaciones.prestacion_form")) # Redirige al mismo endpoint y evita re-envios del form si el user refresca la pagina

# =======================
# API REST
# =======================

@bp.route("/api/prestacion", methods=["GET"], endpoint="api_prestacion_list")
def api_listar_prestacion():
    prestaciones = current_app.prestacion_service.list()

    # prestaciones es list[Prestacion] que trae el service.
    # Convertís cada objeto de dominio a JSON un diccionario simple, serializable.
    data = [
        {
            "id": p.id,
            "nombre": p.name
        }
        for p in prestaciones
    ]

    return jsonify(data), 200 # devuelve una tupla (response, status_code)

# A - El request ya no llega al caso de uso si el usuario no está autenticado.
#     Capa intermedia entre la petición HTTP y la función real de la ruta.
# B - El endpoint lo define Flask como la concatenación del nombre del Blueprint y de la Funcion
# C - URL Path - Asocia la url (viene del base.html) a la funcion "prestaciones"