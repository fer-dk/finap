from app.domain.entities.user import User
from app.domain.entities.log import Log
from app.domain.entities.prestacion import Prestacion
from app.domain.entities.user_credentials import UserCredentials
from abc import ABC, abstractmethod

# Abstract Base Classes
class PrestacionRepoPort(ABC): #A
    @abstractmethod #B
    def insert(self, prestacion: Prestacion) -> Prestacion:
        pass

    @abstractmethod # Devuelve una todas las prestaciones de dominio
    def list(self) -> list[Prestacion]:
        pass

class LogsRepoPort(ABC):
    @abstractmethod
    def register(self, log:Log) -> Log:
        pass

    @abstractmethod
    def list(self) -> list[Log]:
        pass

class UserRepoPort(ABC):
    @abstractmethod
    def find_by_username(self, username: str): # Login
        pass

    @abstractmethod
    def create_user(self, username: str, password_hash: str, role: str = "user") -> User: # C
        pass

    @abstractmethod
    def find_credentials_by_username(self, username: str) -> UserCredentials:
        pass

    @abstractmethod
    def find_by_email(self, username:str) -> User:
        pass

    @abstractmethod
    def list_users(self) -> list[User]:
        pass

class UnitOfWorkPort(ABC):
    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass


# A - ABC Define una interfaz común con métodos que las clases heredadas
#     (PrestacionRepo) deben implementar (codificar)

# B - obligamos con @abstractmethod a que sea implementado por
#     cualquier adaptador(repos, servicios externos).

# C - Aqui sí usamos "-> User" , estás diciendo: "Si me das estos datos, te garantizo que te devolveré una instancia de User recién creada".
#     Aquí no hay ambigüedad (o se crea, o el programa lanza una excepción),
#     por lo que es más fácil y seguro definir el tipo de retorno.


# En arquitectura en capas / hexagonal / clean architecture:
# TODOS los métodos del Port deben ser abstractos.
# En un port es raro que un metodo no sea obligatorio (pero puede no serlo)
