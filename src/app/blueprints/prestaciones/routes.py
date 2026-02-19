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
    # Aquí estás en la capa HTTP: leés datos de la request
    namePres = (request.form.get("nombrePrestacion") or "").strip()
    if not namePres:
        flash("Debe ingresar un nombre.", "warning")
        return redirect(url_for("prestaciones.prestacion_form"))

    # Adaptador HTTP: llama al caso de uso y pasa los objetos de dominio a la vista
    service = current_app.prestacion_service
    service.crear(namePres)
    flash("Registro y Log con éxito", "success")
    return redirect(url_for("prestaciones.prestacion_form")) # Redirige al mismo endpoint y envita re-envíos del form si el user resfresca la pagina


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