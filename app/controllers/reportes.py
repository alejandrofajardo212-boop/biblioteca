from datetime import date
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from app.models.libro import Libro, libro_categoria
from app.models.autor import Autor
from app.models.categoria import Categoria
from app.models.socio import Socio
from app.models.prestamo import Prestamo

def libros_mas_prestados(db: Session, limite: int = 5):
    query = (
        db.query(
            Libro.titulo,
            Autor.nombre.label("autor"),
            func.count(Prestamo.id).label("total_prestamos")
        )
        .join(Autor, Libro.autor_id == Autor.id)
        .outerjoin(Prestamo, Prestamo.libro_id == Libro.id)
        .group_by(Libro.id, Libro.titulo, Autor.nombre)
        .order_by(desc("total_prestamos"))
        .limit(limite)
        .all()
    )
    return [{"titulo": r[0], "autor": r[1], "total_prestamos": r[2]} for r in query]

def libros_por_categoria(db: Session):
    total = func.count(libro_categoria.c.libro_id).label("total_libros")
    query = (
        db.query(Categoria.nombre, total)
        .outerjoin(libro_categoria, libro_categoria.c.categoria_id == Categoria.id)
        .group_by(Categoria.id, Categoria.nombre)
        .all()
    )
    return [{"categoria": r[0], "total_libros": r[1]} for r in query]

def prestamos_vencidos(db: Session):
    hoy = date.today()
    query = (
        db.query(
            Prestamo.id,
            Libro.titulo,
            Socio.nombre,
            Socio.email,
            Prestamo.fecha_limite
        )
        .join(Libro, Prestamo.libro_id == Libro.id)
        .join(Socio, Prestamo.socio_id == Socio.id)
        .filter(Prestamo.fecha_devolucion.is_(None), Prestamo.fecha_limite < hoy)
        .all()
    )
    return [
        {
            "prestamo_id": r[0],
            "titulo": r[1],
            "socio": r[2],
            "email": r[3],
            "fecha_limite": r[4],
            "dias_retraso": (hoy - r[4]).days
        }
        for r in query
    ]

def socios_con_multas(db: Session):
    query = (
        db.query(
            Socio.id,
            Socio.nombre,
            func.sum(Prestamo.multa).label("total_multas"),
            func.count(Prestamo.id).label("prestamos_con_multa")
        )
        .join(Prestamo, Prestamo.socio_id == Socio.id)
        .filter(Prestamo.multa > 0)
        .group_by(Socio.id, Socio.nombre)
        .having(func.sum(Prestamo.multa) > 0)
        .all()
    )
    return [
        {
            "socio_id": r[0],
            "socio": r[1],
            "total_multas": float(r[2]),
            "prestamos_con_multa": r[3]
        }
        for r in query
    ]

def estadisticas_autores(db: Session):
    query = (
        db.query(
            Autor.nombre.label("autor"),
            func.count(func.distinct(Libro.id)).label("total_libros"),
            func.coalesce(func.sum(Libro.ejemplares), 0).label("total_ejemplares"),
            func.count(func.distinct(Prestamo.id)).label("total_prestamos")
        )
        .outerjoin(Libro, Autor.id == Libro.autor_id)
        .outerjoin(Prestamo, Libro.id == Prestamo.libro_id)
        .group_by(Autor.id, Autor.nombre)
        .all()
    )
    return [
        {
            "autor": r[0],
            "total_libros": r[1],
            "total_ejemplares": r[2],
            "total_prestamos": r[3]
        }
        for r in query
    ]

def resumen_general(db: Session):
    hoy = date.today()
    total_libros = db.query(func.count(Libro.id)).scalar() or 0
    total_ejemplares = db.query(func.coalesce(func.sum(Libro.ejemplares), 0)).scalar() or 0
    total_prestados = db.query(func.count(Prestamo.id)).filter(Prestamo.fecha_devolucion.is_(None)).scalar() or 0
    total_socios_activos = db.query(func.count(Socio.id)).filter(Socio.activo.is_(True)).scalar() or 0
    total_vencidos = db.query(func.count(Prestamo.id)).filter(Prestamo.fecha_devolucion.is_(None), Prestamo.fecha_limite < hoy).scalar() or 0
    total_multas = float(db.query(func.coalesce(func.sum(Prestamo.multa), 0.0)).scalar() or 0.0)

    return {
        "total_libros": total_libros,
        "total_ejemplares": total_ejemplares,
        "total_prestados": total_prestados,
        "total_socios_activos": total_socios_activos,
        "total_vencidos": total_vencidos,
        "total_multas": total_multas
    }