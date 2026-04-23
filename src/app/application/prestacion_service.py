#APLICACION
import getpass
from app.domain.entities.prestacion import Prestacion
from app.domain.ports import PrestacionRepoPort, LogsRepoPort

# Servicio de aplicación = capa de CASOS DE USO
class PrestacionService:
    def __init__(self,repoPrest: PrestacionRepoPort, repoLogs: LogsRepoPort):
        self.prest = repoPrest
        self.logs = repoLogs

    # Caso de uso: Crear prestación
    def crear(self, name:str) -> Prestacion:
        prestacion = Prestacion(name = name)

        self.logs.registrar(user=getpass.getuser(), action=f"Inserción Prestación ({prestacion.name})")
        return self.prest.insertar(prestacion) # Aquí el service recibe y devuelve el modelo de dominio

    def listar(self):
        return self.prest.listar()