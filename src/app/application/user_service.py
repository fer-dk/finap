from werkzeug.security import generate_password_hash
from app.domain.entities.user import User
from app.domain.ports import UserRepoPort, UnitOfWorkPort

class UserService:
    def __init__(self, user:UserRepoPort, uow:UnitOfWorkPort):
        self.repoUser=user
        self.repoUow=uow

    def register_user(
            self,
            username: str,
            password: str,
            first_name: str,
            last_name:str,
            email:str,
            role: str = "user") -> User:

        # Reglas de autenticación (que necesitan infraestructura)
        if not password:
            raise ValueError("La contraseña es obligatoria.")
        if self.repoUser.find_by_username(username):
            raise ValueError("El usuario ya existe.")
        if self.repoUser.find_by_email(email):
            raise ValueError("El email ya se encuentra registrado.")

        # Valida el username/email ingresado
        user_new = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role
            )

        password_hash = generate_password_hash(password)

        # Retorno
        try:
            user = self.repoUser.create_user(user=user_new, password_hash=password_hash)
            self.repoUow.commit()       # <-- 1. Esto puede fallar por razones técnicas
            return user
        except Exception:               # <-- 2. Atrapas CUALQUIER fallo técnico inesperado
            self.repoUow.rollback()     # <-- 3. Limpias la base de datos para no dejarla corrupta
            raise                       # <-- 4. Volver a lanzar el error hacia arriba

    def list_users(self) -> list[User]:
        return self.repoUser.list()