from app import create_app
import os

app = create_app() # usamos la factory

def _read_version() -> str: # A
    #Buscamos el directorio donde se encuentra wsgi.py
    base_dir = os.path.dirname(os.path.abspath(__file__)) # B
    version_path = os.path.join(base_dir, "VERSION.txt") # C

    try:
        with open(version_path, "r", encoding="utf-8") as f: # D
            return f.readline().strip() or "unknown" # E
    except OSError: #F
        return "unknown"

app.config["APP_VERSION"] = _read_version() #G

# A - "_read.." indica que la funcion existe para uso interno del modulo, no para ser importada desde otro lado


# B -  "__file__" variable especial python. Contiene la ruta del archivo actual que se está ejecutando. Se usa para construir rutas relativas al archivo.
#                 puede ser absoluta "C:\\Users\\A988021\\Desktop\\FINAP_DEV\\wsgi.py" . La Abolutidad depende del origen de la ruta siempre empieza desde la raiz
#                 puede ser relativa "wsgi.py" . Aquí depende del directorio actual de ejecucio(working directory)
#
#     "os.path.abspath" garantiza que file no dependa del directorio desde donde se ejecuta el proceso. Normaliza y fuerza absotulidad
#
#     "os.path.dirname" en base a la ruta genereada por os.path.abspath ubicamos los archivos relativos de dicha ruta, y los guardamos en base_dir


# C - "os.path.join" construye una ruta correcta. Concatena e inserta "/" o "\" según el SO. Evitando errores


# D - "open" abre el archivo, "as f" asigna el objeto archivo a la variable f
#
#        "f" es un objeto archivo (TextIOWrapper), no un string. Lee el archivo de forma controlada
#
#     "with" es un context manager. Administra un recurso automaticamente, en este caso el archivo abierto.
#            garantiza que se cierre, incluso si hay errores.

# E - "f.readline()" lee una sola linea del archivo y devuelve "1.3.0\n"
#          "strip()" elimina espacios, \n y tabs

# F - "OSError" es una excepción base del sistema operativo(Archivo inexistente, Permisos insuficientes, Path invalido)
#               es una subclase porque herea de Exception y agrupa errores relacionados con el SO.

# G - 'app.config["APP_VERSION"]'
#      es una configuracion interna de Flask, no una variable de entorno. Guarda el valor del objeto Flask para acceso Global
#      Centraliza configuracion, es accesible desde vistas templates, blueprints.
