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
            first_name = user_model.first_name,
            last_name=user_model.last_name,
            email=user_model.email,
            role = user_model.role,
            is_active = user_model.is_active
        )

    def create_user(self, user:User, password_hash:str) -> User:
        user_model = UserModel(
            id=user.id,
            username=user.username,
            first_name=user.firstname,
            last_name=user.lastname,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            password_hash=password_hash
            )

        self.db.session.add(user_model)
        return user

    def find_credentials_by_username(self, username: str) -> UserCredentials | None:
        user_model = UserModel.query.filter_by(username = username).first()

        if user_model is None:
            return None

        user = User(
            id = user_model.id,
            username = user_model.username,
            first_name = user_model.first_name,
            last_name=user_model.last_name,
            email=user_model.email,
            role = user_model.role,
            is_active = user_model.is_active
        )

        return UserCredentials(user=user, password_hash=user_model.password_hash)

    def find_by_email(self, email) -> User | None:
        user_model = UserModel.query.filter_by(email=email).first()

        if user_model is None:
            return None

        return User(
            id = user_model.id,
            username = user_model.username,
            first_name = user_model.first_name,
            last_name=user_model.last_name,
            email=user_model.email,
            role = user_model.role,
            is_active = user_model.is_active
        )

    def list_users(self) -> list[User]:
        rows = UserModel.query.order_by(UserModel.id.desc()).all()
        users : list[User] = []

        for row in rows:
            user = User(
                username=row.username,
                first_name=row.first_name,
                last_name=row.last_name,
                email=row.email,
                role=row.role,
                is_active=row.is_active,
                id=row.id
            )

            users.append(user)

        return users

# A - NO pasamos como parametro una entidad User, ya que al pedir sólo el username
#     no tiene sentido construir una entidad sabiendo que para "buscar" solo necesitamos username

# Al haber migrado a la filosofía de UUIDs, el ID de tipo cadena ya viene creado y
# listo desde el corazón del Dominio (la entidad User). Como el repositorio ya conoce la identidad definitiva
# del usuario antes de guardarlo, no tiene ninguna necesidad de interrumpir el flujo
# para preguntarle a SQLite qué número le va a tocar.