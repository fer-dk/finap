from app.domain.ports import UnitOfWorkPort

class Uowork(UnitOfWorkPort):
    def __init__(self, db):
        self.db = db

    def commit(self) -> None:
        self.db.session.commit()

    def rollback(self) -> None:
        self.db.session.rollback()