# run.py (único para DESA y FINAP)
import os
import sys
# print (sys.path)
import threading
import webbrowser

# Parche: asegurar que FINAP/src esté en sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # Calcula ruta absoluta ""...\FINAP"
SRC_DIR = os.path.join(BASE_DIR, "src")                 # ...\FINAP\src
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)                         # Inserta esa ruta en la primer posicion del sys.path (lo primero que python va a ver)

from wsgi import app                                    # Python busca SRC_DIR (...\FINAP\src) y encuentra a wsgi.py

def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000/") # la app ocupa esa terminal

# Imprime endpoints registrados (solo en modo debug)
def _print_endpoints(app):
    print("\n------ Endpoints --------\n")
    for rule in app.url_map.iter_rules():
        methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
        print(f"{rule.endpoint:<35} → {rule.rule:<25} [ {methods} ]")
    print("\n-------------------------\n")


if __name__ == "__main__":
    # Decide Modo
    mode = os.getenv("APP_MODE", "develpoment").lower() # cambiar a "production" o "developtment"
    debug = (mode == "development")

    print(f"[INFO] Modo: {mode.upper()}")

    # Abre navegadors
    threading.Timer(1.5, abrir_navegador).start()

    # Decide servidor
    if debug:
        _print_endpoints(app)
        app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=True)
    else:
        from waitress import serve
        serve(app, host="127.0.0.1", port=5000, threads=8)