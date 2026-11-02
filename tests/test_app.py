
from datetime import datetime, timezone

from app import create_app
from app.config import TestConfig

# TEST 1: Verificar la configuración de testing
def test_app():
    app = create_app(TestConfig)

    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


# TEST 2: Acceso a una ruta protegida SIN autenticación
def test_protected_route_without_login():
    app = create_app(TestConfig)
    client = app.test_client()

    # Simulamos una solicitud sin haber iniciado sesión
    response = client.get("/prestacion")

    # FINAP debe redirigir al formulario de login
    assert response.status_code == 302
    assert response.headers.get("Location") == "/login?next=/prestacion"


# TEST 3: Acceso a una ruta protegida CON sesión autenticada
def test_protected_route_with_login():
    app = create_app(TestConfig)
    client = app.test_client()

    now = datetime.now(timezone.utc).timestamp()

    # Simulamos una sesión ya iniciada, sin ejecutar el login
    with client.session_transaction() as session: # A
        session["user_id"] = 1
        session["username"] = "user_test"
        session["role"] = "user"
        session["login_at"] = now
        session["last_activity"] = now
    # Salido del with se produce la serialización de los datos

    # Solicitamos la ruta con la sesión autenticada
    response = client.get("/prestacion")

    # Inspeccionamos la respuesta antes de definir los assert
    print("Estado HTTP:", response.status_code)
    print("Redirección:", response.headers.get("Location"))


# A - Paso 1: El inicio (Deserialización inversa / Preparación)
#     Cuando el test arranca, el objeto client (el navegador simulado) está vacío y no tiene cookies.
#     Al ejecutar with client.session_transaction() al no haer nada Flask deserializa un string vacío
#     entrega un diccionario de Python completamente limpio y vacío en la variable session.
#   - Paso 2: Silulación, carga los datos datos de c/atributo en el diccionario ( en memoria)
#   - Paso 3: Serializacion de la cookie