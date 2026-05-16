from werkzeug.security import generate_password_hash, check_password_hash

from app.domain.entities.user import User
from app.domain.entities.user_credentials import UserCredentials
from app.domain.ports import UserRepoPort

class AuthService:
    def __init__(self, repoUser: UserRepoPort, db):
        self.user_repo = repoUser
        self.db = db

    def register_user(self,username: str, password: str, role: str = "user" ) -> User:
        # Reglas de autenticación
        username = (username or "").strip()
        if not username:
            raise ValueError("El usuario es obligatorio.")
        if not password:
            raise ValueError("La contraseña es obligatoria.")

        existing_user = self.user_repo.find_by_username(username)
        if existing_user:
            raise ValueError("El usuario ya existe")

        password_hash = generate_password_hash(password)

        # Retorno
        try:
            user = self.user_repo.create_user(username=username, password_hash = password_hash, role=role)
            self.db.session.commit()    # <-- 1. Esto puede fallar por razones técnicas
            return user
        except Exception:               # <-- 2. Atrapas CUALQUIER fallo técnico inesperado
            self.db.session.rollback()  # <-- 3. Limpias la base de datos para no dejarla corrupta
            raise                       # <-- 4. Volver a lanzar el error hacia arriba


    def login(self, username: str, password: str) -> User:
        # Reglas de autenticación para usuario
        username = (username or "").strip()
        if not username or password: # A
            raise ValueError("Usuario o contraseña inválidos")

        # Reglas de autenticación para credenciales
        credentials = self.user_repo.find_credentials_by_username(username)
        if credentials is None:
            raise ValueError("Usuario o contraseña inválidos.")
        if credentials.user.is_active:
            raise ValueError("Usuario inactivo.")
        # Compara el password ingresado vs password hasheado
        if not check_password_hash(credentials.password_hash, password):
            raise ValueError("Usuario o contraseña invalidos.")

        return credentials.user

# A - No hace falta declarar una variable "password", python lo evaula
#     direcmente en la condición. "Truthiness"