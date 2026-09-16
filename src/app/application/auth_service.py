from app.domain.entities.user import User
from app.domain.ports import UserRepoPort, UnitOfWorkPort

class AuthService:
    def __init__(self, user: UserRepoPort):
        self.repoUser = user

    def login(self, username: str, password: str) -> User:
        # Reglas de autenticación/aplicación
        # El dominio solo valida objetos completos, no textos sueltos de un formulario
        username = (username or "").strip()
        if not username or not password: # A
            raise ValueError("Usuario o contraseña inválidos")

        # Reglas de autenticación para credenciales
        credentials = self.repoUser.find_credentials_by_username(username)
        if credentials is None:
            raise ValueError("Usuario o contraseña inválidos")
        if not credentials.user.activeControl():
            raise ValueError("Usuario inactivo.")
        # Cuando el usuario es correcto compara el password ingresado vs password hasheado
        if not credentials.passControl(password):
            raise ValueError("Usuario o contraseña invalidos")

        return credentials.user

# Retornar el User sin contraseña protege tu aplicación contra filtraciones de seguridad
# y mantiene a tu objeto de dominio puro, representando solo lo que el usuario es y no cómo se autentica.