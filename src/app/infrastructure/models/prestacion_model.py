from app import db
from sqlalchemy import Uuid

class PrestacionModel(db.Model):
    __tablename__ = "prestaciones" # atributo de clase q solo indica la tabla a mapear

    id = db.Column(Uuid(as_uuid=True), primary_key=True)
    name = db.Column(db.String(255), nullable=False) # Fuerza restriccion con False