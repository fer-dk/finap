from app.domain.entities.user import User
from app.domain.entities.user_credentials import UserCredentials
from app.domain.ports import UserRepoPort
from app.infrastructure.models.user_model import UserModel

class UserRepo(UserRepoPort):
    def __init__(self, db):
        self.db = db

    def find_by_username(self, username:str): #A
        user_model = UserModel.query.filter_by(username = username).first()

        if user_model is None:
            return None
        # Adaptador en accion
        return User(
            id = user_model.id,
            username = user_model.username,
            role = user_model.role,
            is_active = user_model.is_active
        )

    def create_user(self, user:User, password_hash:str) -> User:
        user_model = UserModel(
            id=user.id,
            username=user.username,
            role=user.role,
            is_active=user.is_active,
            password_hash=password_hash
            )

        self.db.session.add(user_model)

        return User(
            id = user_model.id,
            username = user_model.username,
            role = user_model.role,
            is_active = user_model.is_active
        )

    def find_credentials_by_username(self, username: str) -> UserCredentials | None:
        user_model = UserModel.query.filter_by(username = username).first()

        if user_model is None:
            return None

        user = User(
            id = user_model.id,
            username = user_model.username,
            role = user_model.role,
            is_active = user_model.is_active
        )

        return UserCredentials(user=user, password_hash=user_model.password_hash)

# A - NO pasamos como parametro una entidad User, ya que al pedir sólo el username
#     no tiene sentido construir una entidad sabiendo que para "buscar" solo necesitamos username

# Al haber migrado a la filosofía de UUIDs, el ID de tipo cadena ya viene creado y
# listo desde el corazón del Dominio (la entidad User). Como el repositorio ya conoce la identidad definitiva
# del usuario antes de guardarlo, no tiene ninguna necesidad de interrumpir el flujo
# para preguntarle a SQLite qué número le va a tocar.