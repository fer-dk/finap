from datetime import datetime

# Representa un registro de log en el dominio
# los parametros deben ser igual a las variables del repo
class Log:
    def __init__(self, id: int, usuario: str, accion: str, fecha_hora: datetime):
        self.id = id
        self.usuario = usuario
        self.accion = accion
        self.fecha_hora = fecha_hora

        # En el caso fecha_hora el tipo en Python no tiene q coincidir con el tipo en SQLite
        # El repositorio hace la conversión al guardar y leer. Se encarga de traducir entre DB y modelo