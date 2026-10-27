from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import paginacion_params
from app.schemas.prestamo import PrestamoOut, PrestamoCreate, DevolucionCreate
from app.controllers import prestamo as controller_prestamo

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])

@router.get("", response_model=list[PrestamoOut])
def listar(
    estado: str | None = None,
    socio_id: int | None = None,
    libro_id: int | None = None,
    pag: dict = Depends(paginacion_params),
    db: Session = Depends(get_db)
):
    return controller_prestamo.listar_prestamos(
        db,
        skip=pag["skip"],
        limit=pag["limit"],
        estado=estado,
        socio_id=socio_id,
        libro_id=libro_id
    )

@router.get("/{id}", response_model=PrestamoOut)
def obtener(id: int, db: Session = Depends(get_db)):
    return controller_prestamo.obtener_prestamo(db, id)

@router.post("", response_model=PrestamoOut, status_code=status.HTTP_201_CREATED)
def crear(prestamo: PrestamoCreate, db: Session = Depends(get_db)):
    return controller_prestamo.crear_prestamo(db, prestamo)

@router.post("/{id}/devolucion", response_model=PrestamoOut)
def devolver(id: int, devolucion: DevolucionCreate, db: Session = Depends(get_db)):
    return controller_prestamo.registrar_devolucion(db, id, devolucion)