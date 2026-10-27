from datetime import date
from pydantic import BaseModel

class ReporteLibroMasPrestado(BaseModel):
    titulo: str
    autor: str
    total_prestamos: int

class ReporteCategoria(BaseModel):
    categoria: str
    total_libros: int

class ReportePrestamoVencido(BaseModel):
    prestamo_id: int
    titulo: str
    socio: str
    email: str
    fecha_limite: date
    dias_retraso: int

class ReporteSocioMulta(BaseModel):
    socio_id: int
    socio: str
    total_multas: float
    prestamos_con_multa: int

class ReporteAutor(BaseModel):
    autor: str
    total_libros: int
    total_ejemplares: int
    total_prestamos: int

class ReporteResumen(BaseModel):
    total_libros: int
    total_ejemplares: int
    total_prestados: int
    total_socios_activos: int
    total_vencidos: int
    total_multas: float