from fastapi import FastAPI, Request, Depends, HTTPException, Response, status
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from models.model import Entry, User
import datetime
from database_API.dependencies import get_db
from database_API.db_operations import init_db
from database_models import database_model
from sqlalchemy.orm import Session
from auth_utils import get_password_hash, create_access_token, verify_password



#Declaracion de objetos y dependencias
app = FastAPI()
init_db()
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
        (database_model.Entry.tittle.contains(query)) | 
        (database_model.Entry.content.contains(query))
    ).all()
    return results




# --- RUTAS DE TAGS ---

@app.get("/tags/") 
async def get_tags(db: Session = Depends(get_db)):
    return db.query(database_model.Tag).all()

@app.get("/tags/{tag_id}/entries")
async def get_entries_by_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(database_model.Tag).filter(database_model.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag no encontrado")
    return tag.entries




# --- RUTAS DE Login y Register---

@app.post("/login")
async def login(user_data: User, db: Session = Depends(get_db)):
    # 1. Buscamos al usuario por su username en Postgres
    user = db.query(database_model.User).filter(database_model.User.username == user_data.username).first()
    
    # 2. Verificamos si el usuario existe
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario o contraseña incorrectos"
        )

    # 3. COMPARACIÓN SEGURA: Comparamos la clave plana con el hash de la DB
    # La función verify_password se encarga de todo el proceso matemático
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario o contraseña incorrectos"
        )

    # 4. Si llegó acá, las credenciales son válidas. Generamos el JWT de 24hs.
    # Metemos el ID y el username en el Payload para "armar la sesión"
    access_token = create_access_token(data={"sub": user.username, "id": user.id})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "username": user.username # Útil para que React sepa a quién saludar
    }

@app.post("/register")
async def register_user(user_data: User, db: Session = Depends(get_db)):
    existing_user = db.query(database_model.User).filter(database_model.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")

    hashed_password = get_password_hash(user_data.password)

    new_user = database_model.User(
        username=user_data.username,
        password=hashed_password  
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "Usuario registrado con éxito", "username": new_user.username}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar el usuario en la base de datos")