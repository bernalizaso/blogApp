from sqlalchemy.orm import Session
from fastapi import HTTPException
from database_models import database_model

class TagController:
    @staticmethod 
    def get_all_tags(db: Session):
            return db.query(database_model.Tag).all()
    @staticmethod
    def get_entries_by_tag(db: Session, tag_id: int):
        tag = db.query(database_model.Tag).filter(database_model.Tag.id == tag_id).first()
        
        if not tag:
            raise HTTPException(
                status_code=404, 
                detail=f"Tag con ID {tag_id} no encontrado"
            )
        return tag.entries