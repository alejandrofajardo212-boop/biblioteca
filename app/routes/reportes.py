from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.reportes import (
    ReporteLibroMasPrestado,
    ReporteCategoria,
    ReportePrestamoVencido,
    ReporteSocioMulta,
    ReporteAutor,
    ReporteResumen
)
from app.controllers import reportes as controller_reportes

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/libros-mas-prestados", response_model=list[ReporteLibroMasPrestado])
def mas_prestados(limite: int = Query(5, ge=1, le=50), db: Session = Depends(get_db)):
    return controller_reportes.libros_mas_prestados(db, limite=limite)

@router.get("/categorias", response_model=list[ReporteCategoria])
def por_categoria(db: Session = Depends(get_db)):
    return controller_reportes.libros_por_categoria(db)

@router.get("/prestamos-vencidos", response_model=list[ReportePrestamoVencido])
def vencidos(db: Session = Depends(get_db)):
    return controller_reportes.prestamos_vencidos(db)

@router.get("/socios-con-multas", response_model=list[ReporteSocioMulta])
def con_multas(db: Session = Depends(get_db)):
    return controller_reportes.socios_con_multas(db)

@router.get("/autores", response_model=list[ReporteAutor])
def autores(db: Session = Depends(get_db)):
    return controller_reportes.estadisticas_autores(db)

@router.get("/resumen", response_model=ReporteResumen)
def resumen(db: Session = Depends(get_db)):
    return controller_reportes.resumen_general(db)