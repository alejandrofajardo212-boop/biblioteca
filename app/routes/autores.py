from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import paginacion_params
from app.schemas.autor import AutorOut, AutorCreate, AutorUpdate
from app.schemas.libro import LibroOut
from app.controllers import autor as controller_autor
from app.controllers import libro as controller_libro

router = APIRouter(prefix="/autores", tags=["Autores"])

@router.get("", response_model=list[AutorOut])
def listar(nacionalidad: str | None = None, pag: dict = Depends(paginacion_params), db: Session = Depends(get_db)):
    return controller_autor.listar_autores(db, skip=pag["skip"], limit=pag["limit"], nacionalidad=nacionalidad)

@router.get("/{id}", response_model=AutorOut)
def obtener(id: int, db: Session = Depends(get_db)):
    return controller_autor.obtener_autor(db, id)

@router.post("", response_model=AutorOut, status_code=status.HTTP_201_CREATED)
def crear(autor: AutorCreate, db: Session = Depends(get_db)):
    return controller_autor.crear_autor(db, autor)

@router.patch("/{id}", response_model=AutorOut)
def actualizar(id: int, autor: AutorUpdate, db: Session = Depends(get_db)):
    return controller_autor.actualizar_autor(db, id, autor)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int, db: Session = Depends(get_db)):
    controller_autor.eliminar_autor(db, id)

@router.get("/{id}/libros", response_model=list[LibroOut])
def libros_del_autor(id: int, pag: dict = Depends(paginacion_params), db: Session = Depends(get_db)):
    autor = controller_autor.obtener_autor(db, id)
    return controller_libro.listar_libros(db, skip=pag["skip"], limit=pag["limit"], autor=autor.nombre)