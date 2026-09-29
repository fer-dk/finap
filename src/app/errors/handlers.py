from flask import render_template, jsonify, request
from app.domain.exceptions.persistence_exceptions import PersistenceError

def register_error_handlers(app):
    # Registra not_found como la función que debe ejecutarse cuando ocurra un error por HTTP 404
    # cuando durante una petición se produzca un HTTP 404

    @app.errorhandler(404) # captura/maneja el error y decide que respuesta enviar.
    def not_found(error): # es el objeto de error que Flask le entrega automáticamente al handler.
        if request.path.startswith("/api/"):
            return jsonify({"error": "not_found", "message": "Recurso no encontrado"}), 404
        return render_template("errors/404.html"), 404 # FLask reconoce(equivale) a una tupla (contenido, status_code y tambien headers)

    @app.errorhandler(403) # significa: estás autenticado, pero no estás autorizado para hacer esto.
    def forbidden(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "forbidden", "message": "No tiene permisos"}), 403
        return render_template("errors/403.html"), 403

    @app.errorhandler(401) # significa en la práctica: ¿Quién sos? Necesitás autenticarte..
    def authentification_required(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "authentification_required", "message": "Debes iniciar sesión"}), 401
        return render_template("errors/401.html"), 401

    @app.errorhandler(400) # La petición HTTP que recibió el servidor no es válida o no puede procesarse correctamente por cómo fue enviada.
    def bad_request(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "bad_request", "message": "Solicitud Incorrecta"}), 400
        return render_template("errors/400.html"), 400

    @app.errorhandler(500)
    def internal_server_error(error): # Maneja un error interno NO ESPERADO, es decir, no tiene un tratamiento especifico. Por lo tanto lo representa como HTTP 500
        if request.path.startswith("/api/"):
            return jsonify({"error": "internal_server_error", "message": "Se produjo un error inesperado"}), 500
        return render_template("errors/500.html"), 500

    @app.errorhandler(PersistenceError)
    def persistence_error(error): # Captura Excepcion (que nosostros definimos y conocemos) Controlada - Error interno del servidor, no es un error http como las anteriores sino que corresponde a un error de Persistencia
        if request.path.startswith("/api/"):
            return jsonify({"error": "persistence_error", "message": "Se produjo un error interno del servidor"}), 500
        return render_template("errors/500.html"), 500


# El Camino del Error (Caso User) - Pila de llamadas:
#   Route llama al service:
#       UserService.register_user()
#   El service llama al UnitOfWork:
#       repoUow.commit()
#   El unit_of_work dentro del except:
#       raise PersistenceError("No fue posible guardar...")
#   Flask recibe la excepción y busca su handler:
#       persistence_error(error)
#   Retorna:
#       return render_template("erros/500.html"), 500