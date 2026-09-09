# Modela:
# autenticación - autorización - seguridad - sesiones futuras - permisos - auditoría
from app import db
from sqlalchemy import Uuid

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(Uuid(as_uuid=True), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user") # permisos mínimos por defecto
    is_active = db.Column(db.Boolean, nullable=False, default=True) # habilitado / deshabilitado
    password_hash = db.Column(db.String(255), nullable=False)# protección irreversible

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now()) # valor automatico
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    last_login_at = db.Column( db.DateTime,nullable=True) # AuthService deberá actualizarlo explícitamente después de autenticar correctamente.
    first_name = db.Column( db.String(80),nullable=False)
    last_name = db.Column( db.String(80),nullable=False)
    email = db.Column( db.String(255),nullable=False,unique=True)
