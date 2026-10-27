class ErrorAplicacion(Exception):
    def __init__(self, mensaje: str, status_code: int = 400):
        self.mensaje = mensaje
        self.status_code = status_code

class NoEncontrado(ErrorAplicacion):
    def __init__(self, mensaje: str = "Recurso no encontrado"):
        super().__init__(mensaje, 404)

class Conflicto(ErrorAplicacion):
    def __init__(self, mensaje: str = "Conflicto con los datos"):
        super().__init__(mensaje, 409)

class ReglaNegocio(ErrorAplicacion):
    def __init__(self, mensaje: str = "Regla de negocio no cumplida"):
        super().__init__(mensaje, 422)