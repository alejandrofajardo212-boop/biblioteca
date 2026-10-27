from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class AutorBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    nacionalidad: Optional[str] = Field(None, max_length=60)
    anio_nacim: Optional[int] = Field(None, ge=1000)

    @field_validator("nombre")
    @classmethod
    def formatear_nombre(cls, v: str) -> str:
        return " ".join(v.split()).title()

    @field_validator("anio_nacim")
    @classmethod
    def validar_anio(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v > date.today().year:
            raise ValueError("El año de nacimiento no puede ser futuro")
        return v

class AutorCreate(AutorBase):
    pass

class AutorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    nacionalidad: Optional[str] = Field(None, max_length=60)
    anio_nacim: Optional[int] = Field(None, ge=1000)

class AutorOut(AutorBase):
    id: int

    class Config:
        from_attributes = True