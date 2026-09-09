from uuid import UUID, uuid4

class User():
    def __init__(
        self,
        id:UUID | None = None,
        username:str = "",
        role:str = "",
        is_active: bool = True
        ):

        username_clean = (username or "").strip()
        if not username_clean:
            raise ValueError("El usuario es obligatorio")

        self.id= id or uuid4()
        self.username= username_clean
        self.role= role
        self.is_active= is_active

    def activeControl(self) -> bool:
        return self.is_active

# Al encapsular la lógica (activeControl) dentro de una función en el dominio, logras tres cosas fundamentales:

# 1. Creas un lenguaje de negocio claro (Ubiquitous Language):
#    En lugar de forzar a tu servicio a leer "banderas electrónicas" (is_active == True),
#    el código ahora habla el idioma de las reglas de tu empresa (user.puede_iniciar_sesion())

# 2. Centralizas la regla de negocio
#    El día de mañana el negocio cambia y la regla se vuelve más compleja.
#    un mismo concepto de negocio suele necesitarse en diferentes partes de la aplicación.
#    Si dejas la lógica de decisión en los servicios (o controladores) en lugar de la entidad, terminas copiando y pegando el mismo if en varios archivos.

# 3. Proteges los datos del objeto (Encapsulamiento)