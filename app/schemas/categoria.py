from typing import Optional
from pydantic import BaseModel, Field, field_validator

class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)

    @field_validator("nombre")
    @classmethod
    def minusculas_nombre(cls, v: str) -> str:
        return " ".join(v.split()).lower()

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)

class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        from_attributes = True