from datetime import datetime

# Representa un registro de log en el dominio
# los parametros deben ser igual a las variables del repo
class Log:
    def __init__(self, id: int, user: str, action: str, datetime: datetime):
        self.id = id
        self.user = user
        self.action = action
        self.datetime = datetime

        # En el caso fecha_hora el tipo en Python no tiene q coincidir con el tipo en SQLite
        # El repositorio hace la conversión al guardar y leer. Se encarga de traducir entre DB y modelo