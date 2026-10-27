from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.schemas.libro import LibroOut
from app.schemas.socio import SocioOut

class PrestamoCreate(BaseModel):
    libro_id: int
    socio_id: int
    fecha_prestamo: Optional[date] = None
    dias: int = Field(14, ge=1, le=30)

    @field_validator("fecha_prestamo")
    @classmethod
    def validar_no_futura(cls, v: Optional[date]) -> Optional[date]:
        if v and v > date.today():
            raise ValueError("La fecha de préstamo no puede ser futura")
        return v

class DevolucionCreate(BaseModel):
    fecha_devolucion: Optional[date] = None

class PrestamoOut(BaseModel):
    id: int
    libro_id: int
    socio_id: int
    fecha_prestamo: date
    fecha_limite: date
    fecha_devolucion: Optional[date] = None
    multa: float
    estado: str
    libro: Optional[LibroOut] = None
    socio: Optional[SocioOut] = None

    class Config:
        from_attributes = True