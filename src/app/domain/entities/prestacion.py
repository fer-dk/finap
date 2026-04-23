from dataclasses import dataclass
from typing import Optional

# Capa Entities – Enterprise business rules
# Modelos de Dominio
@dataclass #A
class Prestacion:
    id: Optional[int] = None
    name: str = ""

    # Regla de negocio: una Prestación sin name no tiene sentido
    def __post_init__(self): #B
        self.name = (self.name or "").strip() #C
        if not self.name:
            raise ValueError("El nombre de la prestación es obligatorio")

# CONCEPTOS ------------

# Prestacion es una entidad de dominio.
# Representa el concepto de negocio "Prestación", no una tabla de base de datos.

# El service y/o el repositorio participan en la construcción y uso
# de la entidad de dominio según el caso de uso.


# ------------------------

# A - crea automaticamente el constructor. Usarlo cuando la clase es sólo un contenedor de datos.

# B - Es un nombre especial y reservado exclusivamente para las @dataclasses.

# C - "Usa el name que me dieron, pero si por alguna razón es nulo, trátalo como un texto vacío para que no falle la limpieza".