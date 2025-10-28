from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    full_name: Optional[str] = Field(None, max_length=100, description="Nombre completo")

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """Schema para crear un usuario"""
    password: str = Field(..., min_length=6, max_length=72, description="Contraseña (6-72 caracteres)")


class User(UserBase):
    """Schema completo de un usuario"""
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema para login"""
    username: str
    password: str


class Token(BaseModel):
    """Schema para el token de autenticación"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Datos contenidos en el token"""
    username: Optional[str] = None
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    full_name: Optional[str] = Field(None, max_length=100, description="Nombre completo")
    id: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    """Schema para crear un usuario"""
    password: str = Field(..., min_length=6, max_length=72, description="Contraseña (6-72 caracteres)")

class UserLogin(BaseModel):
    """Schema para login"""
    username: str
    password: str

class User(UserBase):
    """Schema completo de un usuario"""
    id: int
    is_active: bool
    created_at: datetime
    # Pydantic v2: usar model_config en lugar de class Config
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """Schema para el token de autenticación"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Datos contenidos en el token"""
    username: Optional[str] = None