from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos, Users
from database import SessionLocal
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user, bcrypt_context



router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency =  Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Autenticacion Faliida.-")
    return db.query(Users).filter(Users.id == user.get('id')).first()

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)

class ChangePhoneNumberRequest(BaseModel):
    current_phone_number: str
    new_phone_number: str

@router.post("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, 
    db: db_dependency, 
    user_id: int = Path(gt=0),
    change_password_request: ChangePasswordRequest = None
):
    if user is None:
        raise HTTPException(status_code=401, detail="Autenticacion Fallida.-")
    
    # Verificar que el usuario actual sea el propietario del perfil
    if user.get('id') != user_id:
        raise HTTPException(status_code=403, detail="No tienes permisos para cambiar la contraseña de otro usuario.")
    
    # Obtener el usuario de la base de datos
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if not user_model:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    # Verificar la contraseña actual
    if not bcrypt_context.verify(change_password_request.current_password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta.")
    
    # Hashear y actualizar la nueva contraseña
    user_model.hashed_password = bcrypt_context.hash(change_password_request.new_password)
    db.commit()
    
@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency,
                            db: db_dependency,
                            phone_number: str
                            ):
    if user is None:
        raise HTTPException(status_code=401, detail="Autenticacion Faliida.-")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()  
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()

