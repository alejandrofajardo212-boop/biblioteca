from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

class SocioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, pattern=r"^[0-9+ ]{7,15}$")

    @field_validator("nombre")
    @classmethod
    def formatear_nombre(cls, v: str) -> str:
        return " ".join(v.split()).title()

    @field_validator("email")
    @classmethod
    def email_minusculas(cls, v: str) -> str:
        return v.lower().strip()

class SocioCreate(SocioBase):
    pass

class SocioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, pattern=r"^[0-9+ ]{7,15}$")
    activo: Optional[bool] = None

class SocioOut(SocioBase):
    id: int
    activo: bool
    fecha_alta: datetime

    class Config:
        from_attributes = True