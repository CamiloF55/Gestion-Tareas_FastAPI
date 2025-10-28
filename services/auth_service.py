from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user import User, UserCreate

SECRET_KEY = "tu_clave_secreta_super_segura_cambiala_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.users = []
        self.next_id = 1
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar que la contraseña sea correcta"""
        # Truncar a 72 bytes (límite de bcrypt)
        password_truncated = plain_password[:72]
        return pwd_context.verify(password_truncated, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hashear la contraseña"""
        # Truncar a 72 bytes (límite de bcrypt)
        password_truncated = password[:72]
        return pwd_context.hash(password_truncated)
    
    def get_user_by_username(self, username: str) -> Optional[dict]:
        """Obtener usuario por nombre de usuario"""
        for user in self.users:
            if user["username"] == username:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Obtener usuario por email"""
        for user in self.users:
            if user["email"] == email:
                return user
        return None
    
    def create_user(self, user_data: UserCreate) -> User:
        """Crear un nuevo usuario"""
        hashed_password = self.get_password_hash(user_data.password)
        
        user_dict = {
            "id": self.next_id,
            "username": user_data.username,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        }
        
        self.users.append(user_dict)
        self.next_id += 1
        
        return User(
            id=user_dict["id"],
            username=user_dict["username"],
            email=user_dict["email"],
            full_name=user_dict["full_name"],
            is_active=user_dict["is_active"],
            created_at=user_dict["created_at"]
        )
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autenticar un usuario"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        
        return User(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            full_name=user["full_name"],
            is_active=user["is_active"],
            created_at=user["created_at"]
        )
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token JWT"""
        to_encode = data.copy()
        # usar datetime timezone-aware para evitar DeprecationWarning
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def decode_token(self, token: str) -> Optional[str]:
        """Decodificar token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub")
        except JWTError:
            return None

# Instancia global compartida
auth_service_instance = AuthService()