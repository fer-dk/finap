from werkzeug.security import generate_password_hash
from app.domain.entities.user import User
from app.domain.ports import UserRepoPort, UnitOfWorkPort
from app.domain.exceptions.user_exceptions import UserExistError, EmailExistError

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

        # Validaciones previsibles del caso de uso
        if not password:
            raise ValueError("La contraseña es obligatoria.")
        if self.repoUser.find_by_username(username):
            raise UserExistError("El usuario ya existe.")
        if self.repoUser.find_by_email(email):
            raise EmailExistError("El email ya se encuentra registrado.")

        # Valida el username/email ingresado
        user_new = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role
            )

        password_hash = generate_password_hash(password)
        user = self.repoUser.create_user(user=user_new, password_hash=password_hash) # Retorno

        # Aqui se hace realmente el INSERT, # Puede disparar Fallo inesperado de Integridad
        self.repoUow.commit()
        return user

    def list_users(self) -> list[User]:
        return self.repoUser.list()