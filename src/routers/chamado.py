from distutils.debug import DEBUG
from unicodedata import name
from fastapi import APIRouter, Depends
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
            #falta colocar o do problema do chamado.
        }

models.Base.metadata.create_all(bind=engine)

@router.get("/chamado/", tags=["Chamado"])
def get_chamado(db:Session = Depends(get_db)):
    all_data = db.query(models.Chamado).all()
    return{
        "message":"Dados buscados com sucesso",
        "error": None,
        "data": all_data,
    }

@router.post("/chamado/", tags=["Chamado"])
def post_chamado(data: ChamadoModelo, db: Session = Depends(get_db)):
    ne_object = models.Chamado(**data.dict())
    db.add(new_object)
    db.commit()
    db.refresh(new_object)
    return{
        "message":"Dados buscados com sucesso",
        "error": None,
        "data": new_object,
    }