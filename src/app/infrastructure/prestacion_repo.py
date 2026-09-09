from app.domain.entities.prestacion import Prestacion
from app.domain.ports import PrestacionRepoPort
from app.infrastructure.models.prestacion_model import PrestacionModel

class PrestacionRepo(PrestacionRepoPort): # ADAPTADOR (implementacion) -> Porque es el contenedor que implementa la interfaz (Herencia de INTERFAZ, no herencia clásica)
    def __init__(self, db):
        self.db = db

    # Hasta aqui la entidad ya fue construida
    def insert(self, prestacion: Prestacion) -> Prestacion:
        # Mapeo de dominio
        nueva_prestacion = PrestacionModel(id=prestacion.id, name=prestacion.name)
        self.db.session.add(nueva_prestacion)
        self.db.session.flush() #A

        return Prestacion # no hace falta reconstruirla con los parametros

    def list(self) -> list[Prestacion]:
        rows = PrestacionModel.query.order_by(PrestacionModel.id).all()
        prestaciones:  list[Prestacion] = []

        for row in rows: # por c/interación transforma los objetos en entidades Prestacion
            prest = Prestacion(
                id = row.id,
                name = row.name
            )
            prestaciones.append(prest)

        return prestaciones # Lista de objetos PrestacionModel

# A - ¿Para qué usamos flush() ahora que el ID ya se genera en el dominio?
#
#     Con UUID ya no necesitamos flush() para obtener el ID, porque la entidad
#     Prestacion nace con su identidad antes de llegar al repositorio.
#
#     flush() obliga a SQLAlchemy a enviar las operaciones pendientes a la base
#     de datos dentro de la transacción actual, sin confirmarlas definitivamente.
#
#     Esto permite detectar antes del commit posibles errores de persistencia,
#     como restricciones UNIQUE, FOREIGN KEY, NOT NULL u otros errores del motor.
#
#     El commit(), ejecutado luego mediante el Unit of Work, sigue siendo quien
#     confirma definitivamente la transacción.
#
#     Si posteriormente ocurre un error y se ejecuta rollback(), las operaciones
#     enviadas por flush() se revierten porque todavía no habían sido confirmadas.