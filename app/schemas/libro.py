from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from app.schemas.autor import AutorOut
from app.schemas.categoria import CategoriaOut

class LibroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150)
    isbn: str = Field(..., pattern=r"^\d{13}$")
    anio_publicacion: int = Field(..., ge=1450)
    ejemplares: int = Field(..., ge=1, le=50)

    @field_validator("titulo")
    @classmethod
    def formatear_titulo(cls, v: str) -> str:
        return " ".join(v.split()).title()

    @field_validator("anio_publicacion")
    @classmethod
    def validar_anio(cls, v: int) -> int:
        if v > date.today().year:
            raise ValueError("El año de publicación no puede ser en el futuro")
        return v

class LibroCreate(LibroBase):
    autor_id: int
    categoria_ids: List[int] = Field(..., min_length=1, max_length=5)

    @field_validator("categoria_ids")
    @classmethod
    def validar_categorias_unicas(cls, v: List[int]) -> List[int]:
        if len(v) != len(set(v)):
            raise ValueError("Las categorías no pueden estar duplicadas")
        return v

class LibroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=150)
    isbn: Optional[str] = Field(None, pattern=r"^\d{13}$")
    anio_publicacion: Optional[int] = Field(None, ge=1450)
    ejemplares: Optional[int] = Field(None, ge=1, le=50)
    autor_id: Optional[int] = None
    categoria_ids: Optional[List[int]] = None

class LibroOut(BaseModel):
    id: int
    titulo: str
    isbn: str
    anio_publicacion: int
    ejemplares: int
    disponibles: int
    autor: AutorOut
    categorias: List[CategoriaOut]

    class Config:
        from_attributes = True