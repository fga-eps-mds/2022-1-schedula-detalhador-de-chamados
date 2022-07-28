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

@router.get("/chamado/", tags=["Chamado"])
def get_problem(db:  Session=Depends(get_db)):
    all_data=db.query(models.Problem).all()
    return{
        "message":"Dados buscados com sucesso",
        "error": None,
        "data": all_data,
    }
