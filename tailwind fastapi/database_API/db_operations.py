from .database import SessionLocal, engine
import database_models.database_model as database_model

def init_db():
    print("Creando tablas en la base de datos...")
    database_model.Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        try:
            if db.query(database_model.Tag).count() == 0:
                print("Poblando etiquetas iniciales...")
                default_tags = [
                    database_model.Tag(name="General"),
                    database_model.Tag(name="Programación"),
                    database_model.Tag(name="Tecnología"),
                    database_model.Tag(name="Personal")
                ]
                db.add_all(default_tags)
                db.commit()
                print("Etiquetas creadas con éxito.")
            
            entry_count = db.query(database_model.Entry).count()
            print(f"Base de datos lista. Entradas encontradas: {entry_count}")
            
        except Exception as e:
            db.rollback()
            print(f"Error durante la inicialización de datos: {e}")