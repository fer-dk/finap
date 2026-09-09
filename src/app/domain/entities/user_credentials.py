from werkzeug.security import check_password_hash
from dataclasses import dataclass
from app.domain.entities.user import User

@dataclass
class UserCredentials:
    user: User
    password_hash: str

    def passControl(self, pwd: str) -> bool: # A
        return check_password_hash(self.password_hash, pwd)

# A - Valida criptográficamente si la contraseña ingresada coincide con el hash

# "Un conjunto de credenciales no 'es' un usuario; un conjunto de credenciales contiene a un usuario y
# le añade la contraseña encriptada". Esto mantiene las responsabilidades separadas y el código limpio.

# Seguridad de Negocio:
# El sistema debe exigir que le entregues un usuario real y su contraseña.
# Si faltase alguno, el programa debería fallar de inmediato para evitar dejar una cuenta sin protección.