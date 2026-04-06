#APLICACION
import getpass
from app.domain.ports import PrestacionRepoPort, LogsRepoPort

# Servicio de aplicación = capa de CASOS DE USO
class PrestacionService:
    def __init__(self,repoPrest: PrestacionRepoPort, repoLogs: LogsRepoPort):
        self.prest = repoPrest
        self.logs = repoLogs

    # Caso de uso: Crear prestación
    def crear(self, name:str):
        name  = (name or "").strip()

        if not name: #B
            # Regla de negocio: una Prestación sin name no tiene sentido
            raise ValueError("El nombre de la prestación es obligatorio.")

        # Llamadas LogsRepo (infraestructura)
        self.logs.registrar(user=getpass.getuser(), action=f"Inserción Prestación ({name})")
        # Llamadas PrestacionRepo (infraestructura)
        return self.prest.insertar(name) # Aquí el service recibe y devuelve el modelo de dominio

    def listar(self):
        return self.prest.listar()


# A - "-> Prestacion" es un (type hint) aviso de q esta funcion devuelve un objeto Prestacion (salida)
# B - Regla de negocio: una Prestación sin nombre no tiene sentido