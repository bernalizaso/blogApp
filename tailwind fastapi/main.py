from fastapi import FastAPI, Request, Depends, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from database import session, engine
from models.model import Entry
import datetime
import database_model
from sqlalchemy.orm import Session

#Declaracion de objetos y dependencias
app = FastAPI()
database_model.Base.metadata.create_all(bind=engine)

#arreglo de CORS
origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#aca hay que hacer un refactor

def init_db():

    print("Creando tablas en la base de datos...")
    database_model.Base.metadata.create_all(bind=engine)

    with Session() as db:
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

init_db()

def get_db():
    db = session()
    try:
        yield db #funcion generadora, pausa la ejecucion y luego la continua. Es decir, devuelve el valor de db (en ese caso la sesion de la base de datos), ejecuta y luego sigue al finally que la cierra
    finally:
        db.close()



#Manejo de rutas
#Entradas
@app.post("/")
async def post_entry(entry: Entry, db: Session = Depends(get_db)):
    entry_data = entry.model_dump(exclude={"tags"})
    db_entry = database_model.Entry(**entry_data)
    
    for tag_item in entry.tags:
        db_tag = db.query(database_model.Tag).filter(database_model.Tag.id == tag_item.id).first()
        if db_tag:
            db_entry.tags.append(db_tag) 
    
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.get("/{id}")
async def get_entry(id: int, db: Session = Depends(get_db)):
    db_entry= (db.query(database_model.Entry).filter(database_model.Entry.id == id).first())
    if db_entry:
        return db_entry
    else:
        return "No se pudo encontrar la entrada"


@app.get("/")
async def get_all(db: Session = Depends(get_db) ):
    return db.query(database_model.Entry).all()

@app.delete("/{id}")
async def delete_entry(id : int ,db: Session = Depends(get_db)):
    db_entry= (db.query(database_model.Entry).filter(database_model.Entry.id == id).first())
    if db_entry:
        db.delete(db_entry)
        db.commit()
        return "Entrada borrada exitosamente"
    else:
        return "No se pudo encontrar la entrada"

@app.put("/{id}")
async def edit_entry(id: int, entry: Entry, db: Session = Depends(get_db),  ):
    db_entry= (db.query(database_model.Entry).filter(database_model.Entry.id == id).first())
    if db_entry:
        db_entry.content = entry.content
        db_entry.tittle = entry.tittle
        db.commit()
        return "Entrada editada exitosamente"
    else:
        return "La entrada no ha sido encontrada"

#Manejo de rutas por contenido? verificar si tiene sentido hacer
@app.get("/search/")
async def search_entries(query: str, db: Session = Depends(get_db)):
    results = db.query(database_model.Entry).filter(
        (database_model.Entry.title.contains(query)) | 
        (database_model.Entry.content.contains(query))
    ).all()
    return results




# --- RUTAS DE TAGS ---

@app.get("/tags/", response_model=List[database_model.Tag]) 
async def get_tags(db: Session = Depends(get_db)):
    return db.query(database_model.Tag).all()

@app.get("/tags/{tag_id}/entries")
async def get_entries_by_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(database_model.Tag).filter(database_model.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag no encontrado")
    return tag.entries