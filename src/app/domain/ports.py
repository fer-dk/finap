from app.domain.entities.prestacion import Prestacion
from app.domain.entities.log import Log
from abc import ABC, abstractmethod

# Abstract Base Classes
class PrestacionRepoPort(ABC): #A
    # Guarda una prestacion y devuelve el objeto de dominio
    @abstractmethod #B
    def insertar(self, prestacion: Prestacion)-> Prestacion:
        pass

    # Devuelve una todas las prestaciones de dominio
    @abstractmethod
    def listar(self) -> list[Prestacion]:
        pass

class LogsRepoPort(ABC):
    #Registra una accion en la tabla de logs
    @abstractmethod
    def registrar(self, user: str, action: str):
        pass

    # Devuelve una lista de objetos Log de dominio
    @abstractmethod
    def listar(self) -> list[Log]:
        pass

# A - ABC Define una interfaz común con métodos que las clases heredadas
#     (PrestacionRepo) deben implementar (codificar)

# B - obligamos con @abstractmethod a que sea implementado por
#     cualquier adaptador(repos, servicios externos).

# En arquitectura en capas / hexagonal / clean architecture:
# TODOS los métodos del Port deben ser abstractos.
# En un port es raro que un metodo no sea obligatorio (pero puede no serlo)
