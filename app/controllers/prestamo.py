from datetime import date, timedelta
from sqlalchemy.orm import Session, selectinload
from app.models.prestamo import Prestamo
from app.models.libro import Libro
from app.models.socio import Socio
from app.schemas.prestamo import PrestamoCreate, DevolucionCreate
from app.controllers.libro import calcular_disponibles, formatear_libro_out
from app.core.exceptions import NoEncontrado, Conflicto, ReglaNegocio

def calcular_estado(prestamo: Prestamo) -> str:
    if prestamo.fecha_devolucion is not None:
        return "devuelto"
    if prestamo.fecha_limite < date.today():
        return "vencido"
    return "activo"

def formatear_prestamo(db: Session, p: Prestamo):
    p.estado = calcular_estado(p)
    if p.libro:
        formatear_libro_out(db, p.libro)
    return p

def listar_prestamos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    estado: str | None = None,
    socio_id: int | None = None,
    libro_id: int | None = None
):
    query = db.query(Prestamo).options(
        selectinload(Prestamo.libro).selectinload(Libro.autor),
        selectinload(Prestamo.libro).selectinload(Libro.categorias),
        selectinload(Prestamo.socio)
    )
    if socio_id:
        query = query.filter(Prestamo.socio_id == socio_id)
    if libro_id:
        query = query.filter(Prestamo.libro_id == libro_id)

    hoy = date.today()
    if estado == "devuelto":
        query = query.filter(Prestamo.fecha_devolucion.is_not(None))
    elif estado == "vencido":
        query = query.filter(Prestamo.fecha_devolucion.is_(None), Prestamo.fecha_limite < hoy)
    elif estado == "activo":
        query = query.filter(Prestamo.fecha_devolucion.is_(None), Prestamo.fecha_limite >= hoy)

    prestamos = query.offset(skip).limit(limit).all()
    return [formatear_prestamo(db, p) for p in prestamos]

def obtener_prestamo(db: Session, prestamo_id: int):
    p = db.query(Prestamo).options(
        selectinload(Prestamo.libro).selectinload(Libro.autor),
        selectinload(Prestamo.libro).selectinload(Libro.categorias),
        selectinload(Prestamo.socio)
    ).filter(Prestamo.id == prestamo_id).first()
    if not p:
        raise NoEncontrado("Préstamo no encontrado")
    return formatear_prestamo(db, p)

def crear_prestamo(db: Session, p_in: PrestamoCreate):
    # R1: El socio existe
    socio = db.query(Socio).filter(Socio.id == p_in.socio_id).first()
    if not socio:
        raise NoEncontrado("El socio no existe")

    # R2: El libro existe
    libro = db.query(Libro).filter(Libro.id == p_in.libro_id).first()
    if not libro:
        raise NoEncontrado("El libro no existe")

    # R3: El socio está activo
    if not socio.activo:
        raise ReglaNegocio("El socio no está activo")

    # R4: El socio no tiene préstamos vencidos
    hoy = date.today()
    tiene_vencidos = db.query(Prestamo).filter(
        Prestamo.socio_id == socio.id,
        Prestamo.fecha_devolucion.is_(None),
        Prestamo.fecha_limite < hoy
    ).first()
    if tiene_vencidos:
        raise ReglaNegocio("El socio tiene préstamos vencidos")

    # R5: Menos de 3 préstamos sin devolver
    pendientes = db.query(Prestamo).filter(
        Prestamo.socio_id == socio.id,
        Prestamo.fecha_devolucion.is_(None)
    ).count()
    if pendientes >= 3:
        raise ReglaNegocio("Máximo de 3 préstamos")

    # R6: No tener ese mismo libro sin devolver
    mismo_libro = db.query(Prestamo).filter(
        Prestamo.socio_id == socio.id,
        Prestamo.libro_id == libro.id,
        Prestamo.fecha_devolucion.is_(None)
    ).first()
    if mismo_libro:
        raise Conflicto("El socio ya tiene este libro prestado")

    # R7: Ejemplares disponibles
    if calcular_disponibles(db, libro) <= 0:
        raise ReglaNegocio("No hay ejemplares disponibles")

    # R8: Fechas
    f_prestamo = p_in.fecha_prestamo or hoy
    f_limite = f_prestamo + timedelta(days=p_in.dias)

    nuevo = Prestamo(
        libro_id=libro.id,
        socio_id=socio.id,
        fecha_prestamo=f_prestamo,
        fecha_limite=f_limite,
        multa=0.0
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return obtener_prestamo(db, nuevo.id)

def registrar_devolucion(db: Session, prestamo_id: int, dev_in: DevolucionCreate):
    p = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not p:
        raise NoEncontrado("El préstamo no existe")

    if p.fecha_devolucion is not None:
        raise Conflicto("El préstamo ya fue devuelto")

    f_dev = dev_in.fecha_devolucion or date.today()
    if f_dev < p.fecha_prestamo:
        raise ReglaNegocio("La fecha de devolución no puede ser anterior a la del préstamo")

    p.fecha_devolucion = f_dev

    # R10: Multa = dias * 0.50
    if f_dev > p.fecha_limite:
        dias_retraso = (f_dev - p.fecha_limite).days
        p.multa = dias_retraso * 0.50
    else:
        p.multa = 0.0

    db.commit()
    db.refresh(p)
    return obtener_prestamo(db, p.id)