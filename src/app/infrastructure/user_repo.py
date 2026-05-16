from app.domain.entities.user import User
from app.domain.ports import UserRepoPort
from app.infrastructure.models.user_model import UserModel
from app.domain.entities.user_credentials import UserCredentials

#userrepo = UserRepo(db)
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


    def create_user(self, username:str, password_hash:str, role:str = "user" ) -> User: #B
        user_model = UserModel(username=username, password_hash=password_hash, role=role, is_active=True)
        self.session.add(user_model)
        self.session.flush()

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

# B - Porque no pasamos como parametro a la entidad "User" directamente?
#     Debido a que la entidad 'NO' tiene password_hash, entonces conceptualmente
#     estamos separando "hash" infraestructura/seguridad de la entidad de negocio
#     User mezcla "Dominio - Autenticación - Seguridad" por eso lo separamos en:
#     "User - Credentials - Auth"