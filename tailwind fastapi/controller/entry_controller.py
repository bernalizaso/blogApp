from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.model import Entry
from database_models import database_model

#Si escala tengo que usar __self__ para inyectar dependencia, quedara asi de momento
class EntryController:
    @staticmethod
    def create_entry(db: Session, entry: Entry):
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

    @staticmethod
    def get_all(db: Session):
        return db.query(database_model.Entry).all()

    @staticmethod
    def get_by_id(db: Session, entry_id: int):
        db_entry = db.query(database_model.Entry).filter(database_model.Entry.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="No se pudo encontrar la entrada")
        return db_entry

    @staticmethod
    def delete_entry(db: Session, entry_id: int):
        db_entry = db.query(database_model.Entry).filter(database_model.Entry.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="No se pudo encontrar la entrada")
        db.delete(db_entry)
        db.commit()
        return {"message": "Entrada borrada exitosamente"}

    @staticmethod
    def update_entry(db: Session, entry_id: int, entry_data: Entry):
        db_entry = db.query(database_model.Entry).filter(database_model.Entry.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="La entrada no ha sido encontrada")
        db_entry.content = entry_data.content
        db_entry.tittle = entry_data.tittle
        db.commit()
        return {"message": "Entrada editada exitosamente"}

    @staticmethod
    def search_entries(db: Session, query: str):
        return db.query(database_model.Entry).filter(
            (database_model.Entry.tittle.contains(query)) | 
            (database_model.Entry.content.contains(query))
        ).all()

