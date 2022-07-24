from unicodedata import name
from fastapi import APIRouter
from pydantic import BaseModel

from database import engine
import models
from sqlalchemy.orm import Session

from routers.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

class ChamadoModelo(BaseModel):
    id: str
    name: str
    description = str

    class Config:
        schema_extra = {
            "example": {
                "id": "identificador da categoria",
                "name": "nome da categoria",
                "description": "descricao da categoria",
            }
        }

models.Base.metadata.create_all(bind=engine)


@router.get("/chamado/")
def get_chamado():
    pass

@router.post("/chamado/")
def post_chamado():