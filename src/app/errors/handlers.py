from flask import render_template

def register_error_handlers(app):
    # Registrá not_found como la función que debe ejecutarse cuando ocurra un error HTTP 404
    # cuando durante una petición se produzca un HTTP 404
    @app.errorhandler(404)
    def not_found(error): # es el objeto de error que Flask le entrega automáticamente al handler.
        return render_template("errors/404.html"), 404 # FLask reconoce(equivale) a una tupla (contenido, status_code y tambien headers)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(400) # La petición HTTP que recibió el servidor no es válida o no puede procesarse correctamente por cómo fue enviada.
    def bad_request(error):
        return render_template("errors/400.html"), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500