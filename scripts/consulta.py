from wsgi import app
from app import db
from app.infrastructure.models.user_model import UserModel
from werkzeug.security import generate_password_hash
import uuid


with app.app_context():
    password_plana = "123"

    nuevo_usuario = UserModel(
        id=uuid.uuid4(),
        username="dev",
        role="admin",
        is_active=True,
        password_hash=generate_password_hash(password_plana),
        first_name="Fer",
        last_name="Dk",
        email="deca_06@empresa.com"
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    print("\n[ÉXITO] Usuario creado")
    print(f"Usuario   : {nuevo_usuario.username}")
    print(f"Contraseña: {password_plana}")
    print(f"UUID      : {nuevo_usuario.id}")