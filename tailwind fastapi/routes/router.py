from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_API.dependencies import get_db
from models.model import Entry, User
from controller.entry_controller import EntryController
from controller.auth_controller import AuthController
from controller.tags_controller import TagController

router = APIRouter()

# --- RUTAS DE Entry ---
@router.post("/")
async def post_entry(entry: Entry, db: Session = Depends(get_db)):
    return EntryController.create_entry(db, entry)

@router.get("/")
async def get_all(db: Session = Depends(get_db)):
    return EntryController.get_all(db)

@router.get("/search/")
async def search(query: str, db: Session = Depends(get_db)):
    return EntryController.search_entries(db, query)

@router.get("/{id}")
async def get_one(id: int, db: Session = Depends(get_db)):
    return EntryController.get_by_id(db, id)

@router.delete("/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    return EntryController.delete_entry(db, id)

@router.put("/{id}")
async def edit(id: int, entry: Entry, db: Session = Depends(get_db)):
    return EntryController.update_entry(db, id, entry)

# --- RUTAS DE AUTH ---
@router.post("/login")
async def login(user_data: User, db: Session = Depends(get_db)):
    return AuthController.login(db, user_data)

@router.post("/register")
async def register(user_data: User, db: Session = Depends(get_db)):
    return AuthController.register(db, user_data)

# --- RUTAS DE TAG ---

@router.get("/tags")
async def get_tags(db: Session = Depends(get_db)):
    return TagController.get_all_tags(db)

@router.get("/tags/{tag_id}/entries")
async def get_entries_by_tag(tag_id: int, db: Session = Depends(get_db)):
    return TagController.get_entries_by_tag(db, tag_id)