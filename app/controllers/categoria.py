from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate
from app.core.exceptions import NoEncontrado, Conflicto

def listar_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Categoria).offset(skip).limit(limit).all()

def obtener_categoria(db: Session, categoria_id: int):
    cat = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not cat:
        raise NoEncontrado("Categoría no encontrada")
    return cat

def crear_categoria(db: Session, cat_in: CategoriaCreate):
    if db.query(Categoria).filter(Categoria.nombre == cat_in.nombre).first():
        raise Conflicto("La categoría ya existe")
    nuevo = Categoria(**cat_in.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar_categoria(db: Session, categoria_id: int, cat_in: CategoriaUpdate):
    cat = obtener_categoria(db, categoria_id)
    datos = cat_in.model_dump(exclude_unset=True)
    if "nombre" in datos and datos["nombre"] != cat.nombre:
        if db.query(Categoria).filter(Categoria.nombre == datos["nombre"]).first():
            raise Conflicto("La categoría ya existe")
    for key, val in datos.items():
        setattr(cat, key, val)
    db.commit()
    db.refresh(cat)
    return cat

def eliminar_categoria(db: Session, categoria_id: int):
    cat = obtener_categoria(db, categoria_id)
    db.delete(cat)
    db.commit()