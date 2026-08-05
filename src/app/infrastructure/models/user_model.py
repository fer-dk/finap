# Modela:
# autenticación - autorización - seguridad - sesiones futuras - permisos - auditoría
from app import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    # Permisos
    role = db.Column(
        db.String(50),
        nullable=False,
        default="user" # permisos mínimos por defecto
    )

    # habilitado / deshabilitado
    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    # protección irreversible
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # cuando fue creada la cuenta
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now() # valor automatico
    )

    # ultima modificacion del usuario
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    # Actualiza cuando el usuario inicia session correctamente
    # AuthService deberá actualizarlo explícitamente después de autenticar correctamente.
    last_login_at = db.Column(
        db.DateTime,
        nullable=True
    )

    first_name = db.Column(
        db.String(80),
        nullable=False
    )

    last_name = db.Column(
        db.String(80),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )
