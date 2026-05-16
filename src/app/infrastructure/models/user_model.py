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
