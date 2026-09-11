from werkzeug.security import generate_password_hash
from app.domain.entities.user import User
from app.domain.ports import UserRepoPort, UnitOfWorkPort

class AuthService:
    def __init__(self, user: UserRepoPort, uow:UnitOfWorkPort):
        self.repoUser = user
        self.repoUow = uow

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


    def login(self, username: str, password: str) -> User:
        # Reglas de autenticación/aplicación
        # El dominio solo valida objetos completos, no textos sueltos de un formulario
        username = (username or "").strip()
        if not username or not password: # A
            raise ValueError("Usuario o contraseña inválidos1")

        # Reglas de autenticación para credenciales
        credentials = self.repoUser.find_credentials_by_username(username)
        if credentials is None:
            raise ValueError("Usuario o contraseña inválidos.2")
        if not credentials.user.activeControl():
            raise ValueError("Usuario inactivo.")
        # Cuando el usuario es correcto compara el password ingresado vs password hasheado
        if not credentials.passControl(password):
            raise ValueError("Usuario o contraseña invalidos.3")

        return credentials.user

# Retornar el User sin contraseña protege tu aplicación contra filtraciones de seguridad
# y mantiene a tu objeto de dominio puro, representando solo lo que el usuario es y no cómo se autentica.