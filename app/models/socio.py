from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Socio(Base):
    __tablename__ = "socios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(15), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_alta = Column(DateTime, server_default=func.now())

    prestamos = relationship("Prestamo", back_populates="socio")