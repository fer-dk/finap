from dataclasses import dataclass
from app.domain.entities.user import User

@dataclass
class UserCredentials:
    user: User
    password_hash: str