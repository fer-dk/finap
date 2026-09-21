#APLICACION
import getpass
from app.domain.entities.log import Log
from app.domain.entities.prestacion import Prestacion
from app.domain.ports import PrestacionRepoPort, LogsRepoPort, UnitOfWorkPort

class PrestacionService:
    def __init__(self, prest: PrestacionRepoPort, log: LogsRepoPort, uow: UnitOfWorkPort): # A <--- Implementa el puerto
        self.repoPrest = prest
        self.repologs = log
        self.repoUow = uow

    # Caso de uso: Crear prestación
    def create(self, name:str) -> Prestacion:
        try:
            prestacion = Prestacion(name = name)
            log = Log(user=getpass.getuser(), action=f"Inserción Prestación({prestacion.name})")
            self.repologs.register(log)

            new_prestacion = self.repoPrest.insert(prestacion) # Aqui el service recibe y devuelve el modelo de dominio
            self.repoUow.commit()

            return new_prestacion

        except Exception:
            self.repoUow.rollback()
            raise

    def list(self):
        return self.repoPrest.list()

# A - "Recibo un objeto (repoPrest) que tiene la forma del Puerto."