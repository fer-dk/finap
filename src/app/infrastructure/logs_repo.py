from sqlalchemy import text
from datetime import datetime
from app.domain.entities.logs import Log
from app.domain.ports import LogsRepoPort


class LogsRepo(LogsRepoPort):
    def __init__(self, db):
        self.db = db

    def registrar(self, user: str, action: str):
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.session.execute(
            text("INSERT INTO logs (usuario, accion, fecha_hora) VALUES(:u, :a, :fh)"),
            {"u": user , "a": action, "fh": ahora})
        self.db.session.commit()

    def listar(self) -> list[Log]:
        resultado = self.db.session.execute(
            text("SELECT id, usuario, accion, fecha_hora FROM logs ORDER BY id DESC")
        )
        filas = resultado.fetchall()
        logs: list[Log] = []


        # Convertimos filas en instancias del modelo
        # "El repositorio siempre debe devolver OBJETOS del dominio, no tuplas crudas"

        # Aqui estamos construyendo los parametros que vamos a pasar al constructor.
        # Entonces las variables dentro de log() deben tener el mismo nombre
        # que los parametros definidos en el constructor
        for fila in filas:
            log = Log(
                id=fila.id,
                usuario=fila.usuario,
                accion=fila.accion,
                fecha_hora=fila.fecha_hora
            )
            logs.append(log)

            # Por cada fila crea un objeto log
            # Todos los objetos se guardan en una lista
            # 1 lista de objeto x sql
        return logs

