from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database_API.db_operations import init_db
from routes.router import router 


# Declaracion de objetos y dependencias
app = FastAPI()
init_db()

# arreglo de CORS
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

app.include_router(router)


# Ver httpOnly
#El error 422 es el navegador buscando un favicon que no tengo porque borre static y no me interesa, ignorar
