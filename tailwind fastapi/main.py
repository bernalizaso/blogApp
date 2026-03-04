from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import session, engine
from model import Entry
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

#Ejemplo de entradas para pruebas

ejemplo_entry = [
    Entry(
        id=1,
        date=str(datetime.date.today()),
        tittle="TituloPromedio",
        content="Esto es un contenido promedio",
    ),
    Entry(
        id=2,
        date=str(datetime.date.today()),
        tittle="TituloPromedio2",
        content="Esto es un contenido promedio2",
    ),
    Entry(
        id=3,
        date=str(datetime.date.today()),
        tittle="TituloPromedio3 ",
        content="Esto es un contenido promedio3 ",
    ),
]


#Apertura base de datos

def init_db():
    db = session()
    count = db.query(database_model.Entry).count()
    if count == 0:
        for entry in ejemplo_entry:
            db.add(database_model.Entry(**entry.model_dump()))
        db.commit()

init_db()

def get_db():
    db = session()
    try:
        yield db #funcion generadora, pausa la ejecucion y luego la continua. Es decir, devuelve el valor de db (en ese caso la sesion de la base de datos), ejecuta y luego sigue al finally que la cierra
    finally:
        db.close()



#@app.get("/")
#async def read_home(request: Request):
#    return templates.TemplateResponse("guest/home.html", {"request": request})



#Manejo de rutas
#Entradas
@app.post("/")
async def post_entry(entry: Entry, db: Session = Depends(get_db)):
    db.add(database_model.Entry(**entry.model_dump()))
    db.commit()
    return entry


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



#Manejo de rutas
#Login
# @app.get("/admin")
# async def read_dashboard(request: Request):
#    return templates.TemplateResponse("admin/dashboard.html", {"request": request})
