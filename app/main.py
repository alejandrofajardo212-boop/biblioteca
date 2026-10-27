from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.database import Base, engine
from app.core.exceptions import ErrorAplicacion
from app.routes import autores, categorias, libros, socios, prestamos, reportes 

# Crea las tablas al inicializar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Biblioteca SENA",
    description="Sistema de gestión de préstamos de biblioteca con FastAPI y SQLAlchemy",
    version="1.0.0"
)

# Manejador centralizado de excepciones propias del taller
@app.exception_handler(ErrorAplicacion)
async def aplicacion_exception_handler(request: Request, exc: ErrorAplicacion):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.mensaje}
    )

# Registro de routers
app.include_router(autores.router)
app.include_router(categorias.router)
app.include_router(libros.router)
app.include_router(socios.router)
app.include_router(prestamos.router)
app.include_router(reportes.router)