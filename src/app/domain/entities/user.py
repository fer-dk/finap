from uuid import UUID, uuid4

class User():
    def __init__(
        self,
        username:str,
        first_name:str,
        last_name:str,
        email:str,
        role:str = "user",
        is_active: bool = True,
        id:UUID | None = None
        ):

        username_clean = (username or "").strip()
        first_name_clean = (first_name or "").strip()
        last_name_clean = (last_name or "").strip()
        email_clean = (email or "").strip()
        role_clean = (role or "").strip().lower()

        if not username_clean: raise ValueError("El usuario es obligatorio")
        if not first_name_clean: raise ValueError("El nombre es obligatorio")
        if not last_name_clean: raise ValueError("El apellido es obligatorio")
        if not email_clean: raise ValueError("El email es obligatorio")
        if role_clean not in {"user", "admin"}: raise ValueError("Rol inválido")

        self.id= id or uuid4()
        self.username= username_clean
        self.first_name= first_name_clean
        self.last_name= last_name_clean
        self.email= email_clean
        self.role= role_clean
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