from audioop import add
from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProblemModel(BaseModel):
    id: int
    name: str
    description: str
    active: bool
    updated_at: str
    category_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Falha na conexão com a internet.",
                "description": "Falha ao conectar na internet.",
                "active": True,
                "category_id": 1
            }
        }


models.Base.metadata.create_all(bind=engine)

@router.post("/chamado/", tags=["Chamado"])
def post_chamado(data: ProblemModel, db: Session=Depends(get_db)):
    new_object=models.Problem(**data.dict())
    db.add(new_object)

    db.commit()
    db.refresh(new_object)
    return{
        "message": "Dados buscados com sucesso",
        "error": None,
        "data": new_object,
    }