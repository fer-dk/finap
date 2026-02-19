#INFRAESTRUCTURA
# Gateways = Repositorios → acceden a bases de datos o APIs
from sqlalchemy import text
from app.domain.entities.prestacion import Prestacion
from app.domain.ports import PrestacionRepoPort

# Herencia de INTERFAZ (no herencia clásica)Implementa la interfaz "PrestacionRepoPort" atraves de "herencia"
class PrestacionRepo(PrestacionRepoPort):
    def __init__(self, db):  #A
        # db proviene de la capa Framework & Drivers (SQLAlchemy).
        self.db = db #B

    def insertar(self, nombre: str) -> Prestacion:
        # Acceso directo a la DB (rol de Gateway)
        self.db.session.execute(text("INSERT INTO prestaciones (nombre) VALUES (:n)"), {"n": nombre})
        self.db.session.commit()

        # Convertimos datos externos a entidad de dominio
        return Prestacion(nombre=nombre)


    def listar(self) -> list[Prestacion]:
        resultado = self.db.session.execute(
            text("SELECT id, nombre FROM prestaciones ORDER BY id")
            )
        filas = resultado.fetchall()
        prestaciones:  list[Prestacion] = []

        for fila in filas:
            prest = Prestacion(
                id = fila.id,
                nombre = fila.nombre
            )
            prestaciones.append(prest)

        return prestaciones

# A - "db" en color violeta es una variable que pasamos por parametro, en este caso la variable global "db" (__init__)
# B - "db" en color gris es una propiedad de self a la cual se le asigna "db" (en violeta)