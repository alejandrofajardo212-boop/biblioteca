from app.core.database import SessionLocal, Base, engine
from app.controllers import autor as ctrl_autor
from app.controllers import categoria as ctrl_categoria
from app.controllers import libro as ctrl_libro
from app.controllers import socio as ctrl_socio
from app.schemas.autor import AutorCreate
from app.schemas.categoria import CategoriaCreate
from app.schemas.libro import LibroCreate
from app.schemas.socio import SocioCreate

def reiniciar_y_sembrar():
    print("--- 1. Limpiando y reseteando tablas ---")
    # Borra las tablas existentes y las crea vacías (reinicia los IDs a 1)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Base de datos limpia y lista.")

    db = SessionLocal()
    try:
        print("\n--- 2. Insertando Autores ---")
        autores = [
            {"nombre": "Gabriel García Márquez", "nacionalidad": "Colombiana", "anio_nacim": 1927},
            {"nombre": "Isabel Allende", "nacionalidad": "Chilena", "anio_nacim": 1942},
            {"nombre": "George Orwell", "nacionalidad": "Británica", "anio_nacim": 1903}
        ]
        for a in autores:
            res = ctrl_autor.crear_autor(db, AutorCreate(**a))
            print(f"OK [Autor ID {res.id}]: {res.nombre}")

        print("\n--- 3. Insertando Categorías ---")
        categorias = [
            {"nombre": "novela", "descripcion": "Obras narrativas de ficción extensas"},
            {"nombre": "realismo mágico", "descripcion": "Elementos mágicos en entornos realistas"},
            {"nombre": "distopía", "descripcion": "Sociedades ficticias indeseables"},
            {"nombre": "poesía", "descripcion": "Composición poética"}
        ]
        for c in categorias:
            res = ctrl_categoria.crear_categoria(db, CategoriaCreate(**c))
            print(f"OK [Categoría ID {res.id}]: {res.nombre}")

        print("\n--- 4. Insertando Libros ---")
        libros = [
            {"titulo": "Cien Años De Soledad", "isbn": "9780307474728", "anio_publicacion": 1967, "ejemplares": 2, "autor_id": 1, "categoria_ids": [1, 2]},
            {"titulo": "El Amor En Los Tiempos Del Cólera", "isbn": "9780307387264", "anio_publicacion": 1985, "ejemplares": 1, "autor_id": 1, "categoria_ids": [1]},
            {"titulo": "La Casa De Los Espíritus", "isbn": "9788401343056", "anio_publicacion": 1982, "ejemplares": 2, "autor_id": 2, "categoria_ids": [1, 2]},
            {"titulo": "1984", "isbn": "9780451524935", "anio_publicacion": 1949, "ejemplares": 3, "autor_id": 3, "categoria_ids": [1, 3]}
        ]
        for lib in libros:
            res = ctrl_libro.crear_libro(db, LibroCreate(**lib))
            print(f"OK [Libro ID {res.id}]: {res.titulo}")

        print("\n--- 5. Insertando Socios ---")
        socios = [
            {"nombre": "Ana Torres", "email": "ANA@example.com", "telefono": "+573001234567"},
            {"nombre": "Luis Pérez", "email": "luis@example.com", "telefono": "+573109876543"},
            {"nombre": "Marta Ruiz", "email": "marta@example.com", "telefono": "+573205554433"}
        ]
        for s in socios:
            res = ctrl_socio.crear_socio(db, SocioCreate(**s))
            print(f"OK [Socio ID {res.id}]: {res.nombre}")

        print("\n ¡Datos reiniciados y cargados con éxito desde cero!")

    except Exception as e:
        print(f"\nError durante la carga: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reiniciar_y_sembrar()