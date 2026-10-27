from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import paginacion_params
from app.schemas.categoria import CategoriaOut, CategoriaCreate, CategoriaUpdate
from app.controllers import categoria as controller_categoria

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("", response_model=list[CategoriaOut])
def listar(pag: dict = Depends(paginacion_params), db: Session = Depends(get_db)):
    return controller_categoria.listar_categorias(db, skip=pag["skip"], limit=pag["limit"])

@router.post("", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def crear(cat: CategoriaCreate, db: Session = Depends(get_db)):
    return controller_categoria.crear_categoria(db, cat)

@router.patch("/{id}", response_model=CategoriaOut)
def actualizar(id: int, cat: CategoriaUpdate, db: Session = Depends(get_db)):
    return controller_categoria.actualizar_categoria(db, id, cat)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int, db: Session = Depends(get_db)):
    controller_categoria.eliminar_categoria(db, id)