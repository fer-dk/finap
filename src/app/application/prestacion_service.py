#APLICACION
import getpass
from app.domain.entities.prestacion import Prestacion
from app.domain.ports import PrestacionRepoPort, LogsRepoPort

# Servicio de aplicación = capa de CASOS DE USO
class PrestacionService:
    def __init__(self,repoPrest: PrestacionRepoPort, repoLogs: LogsRepoPort, db):
        self.prest = repoPrest
        self.logs = repoLogs
        self.db = db

    # Caso de uso: Crear prestación
    def crear(self, name:str) -> Prestacion:
        try:
            prestacion = Prestacion(name = name)

            self.logs.registrar(
                user=getpass.getuser(),
                action=f"Inserción Prestación ({prestacion.name})")

            nueva_prestacion = self.prest.insertar(prestacion) # Aquí el service recibe y devuelve el modelo de dominio
            self.db.session.commit() # Service decide las transaccion completa
            return nueva_prestacion

        except Exception:
            self.db.session.rollback()
            raise

    def listar(self):
        return self.prest.listar()