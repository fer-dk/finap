from app import db
from sqlalchemy import Uuid

class LogModel(db.Model):
    __tablename__="logs"

    id = db.Column(Uuid(as_uuid=True), primary_key=True) # A
    user = db.Column(db.String(255), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

# A - "as_uuid" Indica a SQLalchemy que en Python querés trabajar con objetos UUID y entregar objetos uuid.UUID
#     "Esta columna representa UUID y adaptala al dialecto de la base"