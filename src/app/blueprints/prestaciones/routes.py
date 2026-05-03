#CONTROLLERS
from . import bp
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app

# Controlador HTTP / HTML (capa de interfaz)
@bp.route("/prestacion", methods=["GET"], endpoint="prestacion_form") #A,B
def mostrar_form(): # View Fuction
    # Actua como un Presenter
    return render_template("prestaciones/prestacion.html")

@bp.route("/prestacion", methods=["POST"], endpoint="prestacion_insert")
def insertar_prestacion():
    namePres = request.form.get("nombrePrestacion")
    service = current_app.prestacion_service # Adaptador HTTP: llama al caso de uso

    try:
        service.crear(namePres) # pasa los objetos de dominio a la vista
        flash("Registro y Log con éxito", "success")
    except ValueError as e:
        flash(str(e), "warning")
        return redirect(url_for("prestaciones.prestacion_form"))

    return redirect(url_for("prestaciones.prestacion_form")) # Redirige al mismo endpoint y evita re-envíos del form si el user resfresca la pagina


# =======================
# API REST
# =======================

@bp.route("/api/prestacion", methods=["GET"], endpoint="api_prestacion_list")
def api_listar_prestacion():
    service = current_app.prestacion_service
    service = service.listar()

    # prestaciones es list[Prestacion] que trae el service.
    # Convertís cada objeto de dominio a JSON un diccionario simple, serializable.
    data = [
        {
            "id": p.id,
            "nombre": p.nombre
        }
        for p in service
    ]

    return jsonify(data), 200


# A - El endpoint lo define Flask como la concatenación del nombre del Blueprint y de la Funcion
# B - URL Path - Asocia la url (viene del base.html) a la funcion "prestaciones"