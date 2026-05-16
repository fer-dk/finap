#INFRAESTRUCTURA
# Patron de diseño -> Gateways = Repositorios
# Actúa como una "puerta" hacia el mundo exterior
# (bases de datos, APIs de terceros o sistemas de archivos)

# Se importa para usar type hints e instanciar Prestacion.
from app.domain.entities.prestacion import Prestacion
from app.domain.ports import PrestacionRepoPort
from app.infrastructure.models.prestacion_model import PrestacionModel

# ADAPTADOR (implementacion) -> Porque es el contenedor que implementa la interfaz (Herencia de INTERFAZ, no herencia clásica)
class PrestacionRepo(PrestacionRepoPort):
    def __init__(self, db): #A
        self.db = db #B

    def insertar(self, prestacion: Prestacion) -> Prestacion:
        # Traduce la entidad a ORM (Mapping de Dominio)
        nueva_prestacion = PrestacionModel(name=prestacion.name) # Acceso directo a la DB (rol de Gateway)
        self.db.session.add(nueva_prestacion)
        self.db.session.flush() # envia el INSERT a la db sin cerrar la transacción

        # Reconstruye (instanciacion de clase) la Entidad con datos. No se modifica la entidad original, se crea una nueva
        return Prestacion(
            id=nueva_prestacion.id,
            name=nueva_prestacion.name
        )

    def listar(self) -> list[Prestacion]:
        filas = PrestacionModel.query.order_by(PrestacionModel.id).all()
        prestaciones:  list[Prestacion] = []

        for fila in filas:
            prest = Prestacion(
                id = fila.id,
                name = fila.name
            )
            prestaciones.append(prest)
        return prestaciones

# A - db proviene de la capa Framework & Drivers (SQLAlchemy).
# B - "db" en color gris es una propiedad de self a la cual se le asigna "db" (en violeta)