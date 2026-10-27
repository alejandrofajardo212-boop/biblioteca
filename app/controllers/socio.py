from sqlalchemy.orm import Session
from app.models.socio import Socio
from app.models.prestamo import Prestamo
from app.schemas.socio import SocioCreate, SocioUpdate
from app.core.exceptions import NoEncontrado, Conflicto

def listar_socios(db: Session, skip: int = 0, limit: int = 100, activo: bool | None = None):
    query = db.query(Socio)
    if activo is not None:
        query = query.filter(Socio.activo == activo)
    return query.offset(skip).limit(limit).all()

def obtener_socio(db: Session, socio_id: int):
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    if not socio:
        raise NoEncontrado("Socio no encontrado")
    return socio

def crear_socio(db: Session, socio_in: SocioCreate):
    if db.query(Socio).filter(Socio.email == socio_in.email).first():
        raise Conflicto("El email ya está registrado")
    nuevo = Socio(**socio_in.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar_socio(db: Session, socio_id: int, socio_in: SocioUpdate):
    socio = obtener_socio(db, socio_id)
    datos = socio_in.model_dump(exclude_unset=True)
    if "email" in datos and datos["email"] != socio.email:
        if db.query(Socio).filter(Socio.email == datos["email"]).first():
            raise Conflicto("El email ya está registrado")
    for k, v in datos.items():
        setattr(socio, k, v)
    db.commit()
    db.refresh(socio)
    return socio

def eliminar_socio(db: Session, socio_id: int):
    socio = obtener_socio(db, socio_id)
    sin_devolver = db.query(Prestamo).filter(
        Prestamo.socio_id == socio.id,
        Prestamo.fecha_devolucion.is_(None)
    ).count()
    if sin_devolver > 0:
        raise Conflicto("El socio tiene préstamos activos sin devolver")

    total_prestamos = db.query(Prestamo).filter(Prestamo.socio_id == socio.id).count()
    if total_prestamos > 0:
        socio.activo = False
        db.commit()
    else:
        db.delete(socio)
        db.commit()