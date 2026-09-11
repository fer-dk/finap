# Ejecutar de esta forma:
# PYTHONPATH=.:src APP_ENV=DevMysql python3 -m scripts.create_user

from wsgi import app
from getpass import getpass

username = input("Usuario: ").strip()
password = getpass("Constraseña: ")
role = input("Rol [user/admin]: ").strip()
first_name = input("Nombre: ").strip()
last_name = input("Apellido: ").strip()
email = input("Email: ").strip()

with app.app_context(): # crea un objeto de contexto Flask
    user = app.auth_service.register_user(
        username=username,
        password=password,
        role=role,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    print(f"Usuario '{user.username}'creado correctamente")


# “Durante este bloque de código, quiero que Flask considere que estoy trabajando
# dentro del contexto de esta aplicación.”

# Dentro de ese bloque, componentes como Flask-SQLAlchemy pueden acceder al contexto
# de la aplicación y a su configuración.

# with
# │
# ├── sentencia de Python
# │
# app
# │
# ├── objeto Flask
# │
# .app_context()
# │
# └── método del objeto app
#      que devuelve un Context Manager

# Flask diseñó app_context() de manera que sea compatible con el mecanismo with de Python.