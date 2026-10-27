from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import paginacion_params
from app.schemas.socio import SocioOut, SocioCreate, SocioUpdate
from app.schemas.prestamo import PrestamoOut
from app.controllers import socio as controller_socio
from app.controllers import prestamo as controller_prestamo

router = APIRouter(prefix="/socios", tags=["Socios"])

@router.get("", response_model=list[SocioOut])
def listar(activo: bool | None = None, pag: dict = Depends(paginacion_params), db: Session = Depends(get_db)):
    return controller_socio.listar_socios(db, skip=pag["skip"], limit=pag["limit"], activo=activo)

@router.get("/{id}", response_model=SocioOut)
def obtener(id: int, db: Session = Depends(get_db)):
    return controller_socio.obtener_socio(db, id)

@router.post("", response_model=SocioOut, status_code=status.HTTP_201_CREATED)
def crear(socio: SocioCreate, db: Session = Depends(get_db)):
    return controller_socio.crear_socio(db, socio)

@router.patch("/{id}", response_model=SocioOut)
def actualizar(id: int, socio: SocioUpdate, db: Session = Depends(get_db)):
    return controller_socio.actualizar_socio(db, id, socio)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int, db: Session = Depends(get_db)):
    controller_socio.eliminar_socio(db, id)

@router.get("/{id}/prestamos", response_model=list[PrestamoOut])
def prestamos_del_socio(
    id: int,
    estado: str | None = None,
    pag: dict = Depends(paginacion_params),
    db: Session = Depends(get_db)
):
    controller_socio.obtener_socio(db, id)
    return controller_prestamo.listar_prestamos(db, skip=pag["skip"], limit=pag["limit"], estado=estado, socio_id=id)