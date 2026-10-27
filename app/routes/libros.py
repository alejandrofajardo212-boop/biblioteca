from enum import Enum
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import paginacion_params
from app.schemas.libro import LibroOut, LibroCreate, LibroUpdate
from app.controllers import libro as controller_libro

class OrdenEnum(str, Enum):
    titulo = "titulo"
    anio = "anio"
    menos_anio = "-anio"

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.get("", response_model=list[LibroOut])
def listar(
    buscar: str | None = None,
    autor: str | None = None,
    categoria_id: int | None = None,
    desde: int | None = None,
    hasta: int | None = None,
    orden: OrdenEnum | None = None,
    pag: dict = Depends(paginacion_params),
    db: Session = Depends(get_db)
):
    orden_val = orden.value if orden else None
    return controller_libro.listar_libros(
        db,
        skip=pag["skip"],
        limit=pag["limit"],
        buscar=buscar,
        autor=autor,
        categoria_id=categoria_id,
        desde=desde,
        hasta=hasta,
        orden=orden_val
    )

@router.get("/{id}", response_model=LibroOut)
def obtener(id: int, db: Session = Depends(get_db)):
    return controller_libro.obtener_libro(db, id)

@router.post("", response_model=LibroOut, status_code=status.HTTP_201_CREATED)
def crear(libro: LibroCreate, db: Session = Depends(get_db)):
    return controller_libro.crear_libro(db, libro)

@router.patch("/{id}", response_model=LibroOut)
def actualizar(id: int, libro: LibroUpdate, db: Session = Depends(get_db)):
    return controller_libro.actualizar_libro(db, id, libro)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int, db: Session = Depends(get_db)):
    controller_libro.eliminar_libro(db, id)