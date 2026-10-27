from sqlalchemy.orm import Session
from app.models.autor import Autor
from app.schemas.autor import AutorCreate, AutorUpdate
from app.core.exceptions import NoEncontrado, Conflicto

def listar_autores(db: Session, skip: int = 0, limit: int = 100, nacionalidad: str | None = None):
    query = db.query(Autor)
    if nacionalidad:
        query = query.filter(Autor.nacionalidad.ilike(f"%{nacionalidad}%"))
    return query.offset(skip).limit(limit).all()

def obtener_autor(db: Session, autor_id: int):
    autor = db.query(Autor).filter(Autor.id == autor_id).first()
    if not autor:
        raise NoEncontrado("Autor no encontrado")
    return autor

def crear_autor(db: Session, autor_in: AutorCreate):
    if db.query(Autor).filter(Autor.nombre == autor_in.nombre).first():
        raise Conflicto("Ya existe un autor con este nombre")
    nuevo = Autor(**autor_in.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar_autor(db: Session, autor_id: int, autor_in: AutorUpdate):
    autor = obtener_autor(db, autor_id)
    datos = autor_in.model_dump(exclude_unset=True)
    if "nombre" in datos and datos["nombre"] != autor.nombre:
        if db.query(Autor).filter(Autor.nombre == datos["nombre"]).first():
            raise Conflicto("Ya existe un autor con este nombre")
    for key, value in datos.items():
        setattr(autor, key, value)
    db.commit()
    db.refresh(autor)
    return autor

def eliminar_autor(db: Session, autor_id: int):
    autor = obtener_autor(db, autor_id)
    if autor.libros:
        raise Conflicto("No se puede eliminar el autor porque tiene libros asociados")
    db.delete(autor)
    db.commit()