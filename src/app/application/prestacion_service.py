#APLICACION
import os
from app.domain.ports import PrestacionRepoPort, LogsRepoPort

# Servicio de aplicación = capa de CASOS DE USO
class PrestacionService:
    def __init__(self,repo: PrestacionRepoPort, logs: LogsRepoPort):
        self.prest = repo
        self.logs = logs

    # Caso de uso: Crear prestación
    def crear(self, nombre:str):
        nombre  = (nombre or "").strip()

        if not nombre: #B
            # Regla de negocio: una Prestación sin nombre no tiene sentido
            raise ValueError("El nombre de la prestación es obligatorio.")

         # Llamadas a infraestructura y retorno
        self.logs.registrar(user = os.getlogin(), action = f"Inserción Prestación ({nombre})")
        return self.prest.insertar(nombre) # Aquí el service recibe y devuelve el modelo de dominio

    def listar(self):
        return self.prest.listar()


# A - "-> Prestacion" es un (type hint) aviso de q esta funcion devuelve un objeto Prestacion (salida)
# B - Regla de negocio: una Prestación sin nombre no tiene sentido