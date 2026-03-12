from database_models import database_model
from auth_utils import get_password_hash, create_access_token, verify_password
from models.model import  User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

class AuthController:
    @staticmethod
    def login(db: Session, user_data: User):
        user = db.query(database_model.User).filter(database_model.User.username == user_data.username).first()
        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Usuario o contraseña incorrectos"
            )
        
        access_token = create_access_token(data={"sub": user.username, "id": user.id})
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "username": user.username 
        }

    @staticmethod
    def register(db: Session, user_data: User):
        existing_user = db.query(database_model.User).filter(database_model.User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")

        new_user = database_model.User(
            username=user_data.username,
            password=get_password_hash(user_data.password)
        )
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {"message": "Usuario registrado con éxito", "username": new_user.username}
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error al guardar el usuario")