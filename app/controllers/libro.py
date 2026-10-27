from sqlalchemy.orm import Session, selectinload
from app.models.libro import Libro
from app.models.autor import Autor
from app.models.categoria import Categoria
from app.models.prestamo import Prestamo
from app.schemas.libro import LibroCreate, LibroUpdate
from app.core.exceptions import NoEncontrado, Conflicto, ReglaNegocio

def calcular_disponibles(db: Session, libro: Libro) -> int:
    prestamos_activos = db.query(Prestamo).filter(
        Prestamo.libro_id == libro.id,
        Prestamo.fecha_devolucion.is_(None)
    ).count()
    return max(0, libro.ejemplares - prestamos_activos)

def formatear_libro_out(db: Session, libro: Libro):
    libro.disponibles = calcular_disponibles(db, libro)
    return libro

def listar_libros(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    buscar: str | None = None,
    autor: str | None = None,
    categoria_id: int | None = None,
    desde: int | None = None,
    hasta: int | None = None,
    orden: str | None = None
):
    query = db.query(Libro).options(selectinload(Libro.autor), selectinload(Libro.categorias))
    if buscar:
        query = query.filter(Libro.titulo.ilike(f"%{buscar}%"))
    if autor:
        query = query.join(Libro.autor).filter(Autor.nombre.ilike(f"%{autor}%"))
    if categoria_id:
        query = query.join(Libro.categorias).filter(Categoria.id == categoria_id)
    if desde:
        query = query.filter(Libro.anio_publicacion >= desde)
    if hasta:
        query = query.filter(Libro.anio_publicacion <= hasta)

    if orden == "titulo":
        query = query.order_by(Libro.titulo.asc())
    elif orden == "anio":
        query = query.order_by(Libro.anio_publicacion.asc())
    elif orden == "-anio":
        query = query.order_by(Libro.anio_publicacion.desc())

    libros = query.offset(skip).limit(limit).all()
    return [formatear_libro_out(db, lib) for lib in libros]

def obtener_libro(db: Session, libro_id: int):
    libro = db.query(Libro).options(
        selectinload(Libro.autor),
        selectinload(Libro.categorias)
    ).filter(Libro.id == libro_id).first()
    if not libro:
        raise NoEncontrado("Libro no encontrado")
    return formatear_libro_out(db, libro)

def crear_libro(db: Session, libro_in: LibroCreate):
    if not db.query(Autor).filter(Autor.id == libro_in.autor_id).first():
        raise NoEncontrado("El autor especificado no existe")
    if db.query(Libro).filter(Libro.isbn == libro_in.isbn).first():
        raise Conflicto("El ISBN ya está registrado")

    categorias = db.query(Categoria).filter(Categoria.id.in_(libro_in.categoria_ids)).all()
    if len(categorias) != len(libro_in.categoria_ids):
        raise NoEncontrado("Una o más categorías no existen")

    datos = libro_in.model_dump(exclude={"categoria_ids"})
    nuevo = Libro(**datos)
    nuevo.categorias = categorias
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return formatear_libro_out(db, nuevo)

def actualizar_libro(db: Session, libro_id: int, libro_in: LibroUpdate):
    libro = obtener_libro(db, libro_id)
    datos = libro_in.model_dump(exclude_unset=True)

    if "ejemplares" in datos:
        prestamos_activos = db.query(Prestamo).filter(
            Prestamo.libro_id == libro.id,
            Prestamo.fecha_devolucion.is_(None)
        ).count()
        if datos["ejemplares"] < prestamos_activos:
            raise ReglaNegocio("Los ejemplares no pueden ser menores a los préstamos activos")

    if "categoria_ids" in datos:
        cats = db.query(Categoria).filter(Categoria.id.in_(datos["categoria_ids"])).all()
        if len(cats) != len(datos["categoria_ids"]):
            raise NoEncontrado("Una o más categorías no existen")
        libro.categorias = cats
        del datos["categoria_ids"]

    for k, v in datos.items():
        setattr(libro, k, v)

    db.commit()
    db.refresh(libro)
    return formatear_libro_out(db, libro)

def eliminar_libro(db: Session, libro_id: int):
    libro = obtener_libro(db, libro_id)
    activos = db.query(Prestamo).filter(
        Prestamo.libro_id == libro.id,
        Prestamo.fecha_devolucion.is_(None)
    ).count()
    if activos > 0:
        raise Conflicto("No se puede eliminar el libro porque tiene préstamos sin devolver")
    db.delete(libro)
    db.commit()