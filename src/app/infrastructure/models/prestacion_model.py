from app import db

# Existe una tabla prestaciones con estas columnas:
class PrestacionModel(db.Model):
    __tablename__ = "prestaciones" # atributo de clase q solo indica la tabla a mapear

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)