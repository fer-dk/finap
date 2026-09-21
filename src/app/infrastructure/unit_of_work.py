# Objetivo:
# Que el límite transaccional (de infraestructura) traduzca el IntegrityError a esa excepción propia,
# sin exponer SQLAlchemy hacia arriba


# "Unit of work" controla la transaccion, es decir:
# "Cuando confirmo o deshago el conjunto de cambios"

# La db devuelve Error, SQLAlchemy recibe ese error y lo representa como un IntegrityError
from sqlalchemy.exc import IntegrityError

from app.domain.ports import UnitOfWorkPort
from app.domain.exceptions.persistence_exceptions import PersistenceError

class Uowork(UnitOfWorkPort):
    def __init__(self, db):
        self.db = db

    def commit(self) -> None:
        try:
            self.db.session.commit()
        except IntegrityError as e:
            self.db.session.rollback()
            raise PersistenceError("No fue posible guardar los datos por una restricción de integridad.") from e

    #otro caso de uso podría necesitar abortar explícitamente una transacción
    def rollback(self) -> None:
        self.db.session.rollback()