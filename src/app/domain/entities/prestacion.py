from dataclasses import dataclass
from typing import Optional

# Capa Entities – Enterprise business rules
# Modelos de Dominio
@dataclass #A
class Prestacion:
    id: Optional[int] = None
    name: str = ""

# CONCEPTOS ------------

# El modelo es una clase que representa una entidad del dominio del negocio, NO la tabla en sí.
# Modelo de dominio representa qué es una Prestación como concepto del negocio. Es solo el model de un objeto de dominio (Prestacion)
# El "model" aparece de forma explicita cuando definimos la entidad como objeto (dentro routes.py), y service la crea pasandola como parametro

# PrestacionRepository es el motor (acceso a datos)
# PrestacionService es el auto (usa un repo para aplicar reglas)

# No se usa "herencia", sino "composición"
# El Service USA el repositorio.

# ------------------------
#A - crea automaticamente el constructor. Usarlo cuando la clase es sólo un contenedor de datos.