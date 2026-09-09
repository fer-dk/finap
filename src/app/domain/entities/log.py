from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional

# Representa un registro de log en el dominio. Los parametros deben ser igual a las variables del repo
class Log:
    def __init__(
            self,
            user: str,
            action: str,
            id: UUID | None = None, # Ahora el id es un Universally Unique Identifier)
            dt_at: Optional[datetime] = None # tipado de entrada
            ):
            self.id=id or uuid4() # Genera o no un Id aleatorio
            self.user=user
            self.action=action
            self.datetime= dt_at or datetime.now(timezone.utc) # tipado de salida


# Hacemos que el id sea "opcional", pero el ID no es opcional para una entidad válida.
# Lo opcional es que "quien" construye una entidad NUEVA tenga que proporcionar ese ID.

 # La clase Log es un "Objeto de Transferencia" (DTO) es una clase tonta
 # que no tiene ningún comportamiento (cero funciones), y solo sirve para
 # transportar datos limpios entre capas (como un contenedor de plástico).

 # Tipado de Entrada vs Salida
 # El type hint de la firma (constructor) le avisa al programador de turno:
 # "Oye, en el argumento tienes permitido mandarme None (entrada),
 # pero te garantizo que el objeto final que vas a usar no tendrá un valor nulo (salida)"

