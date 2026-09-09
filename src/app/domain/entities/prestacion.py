from uuid import UUID, uuid4
from dataclasses import dataclass, field
from typing import Optional

# Capa Entities – Enterprise business rules
@dataclass #A
class Prestacion:
    name: str = ""
    id: UUID = field(default_factory=uuid4)

    # Regla de negocio
    def __post_init__(self): #B
        self.name = (self.name or "").strip() #C
        if not self.name:
            raise ValueError("El nombre de la prestación es obligatorio")

# Hacemos que el id sea "opcional", pero el ID no es opcional para una entidad válida.
# Lo opcional es que quien construye una entidad NUEVA tenga que proporcionar ese ID.

# A - crea automaticamente el constructor. Usarlo cuando la clase es sólo un contenedor de datos.
# B - Es un nombre especial y reservado exclusivamente para las @dataclasses.