from fastapi import Query

def paginacion_params(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros por página")
) -> dict:
    return {"skip": skip, "limit": limit}