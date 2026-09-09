from datetime import datetime
from app.domain.entities.log import Log
from app.domain.ports import LogsRepoPort
from app.infrastructure.models.log_model import LogModel


class LogRepo(LogsRepoPort):
    def __init__(self, db):
        self.db = db

    def register(self, log: Log) -> Log:
        # 1. Creas el modelo
        log_model = LogModel(id=log.id, user=log.user, action=log.action, datetime=log.datetime)
        # 2. Guardas en la sesión y empujas el cambio para obtener el ID secuencial
        self.db.session.add(log_model)
        # 3. Retornas una ENTIDAD con el ID real
        return Log(
            id=log_model.id,
            user=log_model.user,
            action=log_model.action,
            dt_at=log_model.datetime
        )

    def list(self) -> list[Log]: #A
        rows = LogModel.query.order_by(LogModel.id.desc()).all()
        logs: list[Log] = []

        for row in rows: #B
            log = Log(
                id=row.id,
                user=row.user,
                action=row.action,
                dt_at=row.datetime # 'dt_at' es el parametro del constructor Logy 'row.datetime' es la columna de la DB
            )
            logs.append(log)

        return logs