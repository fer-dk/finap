from datetime import datetime
from app.domain.entities.log import Log
from app.domain.ports import LogsRepoPort
from app.infrastructure.models.log_model import LogModel

class LogRepo(LogsRepoPort):
    def __init__(self, db):
        self.db = db

    def registrar(self, user: str, action: str):
        nuevo_log = LogModel(user=user, action=action, datetime = datetime.now())
        self.db.session.add(nuevo_log) # no hacemos commit pq depende de insertar()

    def listar(self) -> list[Log]: #A
        filas = LogModel.query.order_by(LogModel.id.desc()).all()
        logs: list[Log] = []

        # Convertimos filas en instancias del modelo
        # "El repositorio siempre debe devolver OBJETOS del dominio, no tuplas crudas"
        for fila in filas: #B
            log = Log(
                id=fila.id,
                user=fila.user,
                action=fila.action,
                datetime=fila.datetime
            )
            logs.append(log)

        return logs

# A -  "-> list[Log]"": Indica que el valor de retorno del método será una lista
#      y que cada elemento dentro de esa lista será un objeto de la clase Log

# B -  Aqui estamos construyendo los parametros que vamos a pasar al constructor.
#      Entonces las variables dentro de log() deben tener el mismo nombre
#      que los parametros definidos en el constructor
#      Por cada fila crea un objeto log
#      Todos los objetos se guardan en una lista
#      1 lista de objeto x sql