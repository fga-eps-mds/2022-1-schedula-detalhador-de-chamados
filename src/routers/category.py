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


class CategoryModel(BaseModel):
    id: int
    name: str
    description: str
    active: bool
    updated_at: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Internet",
                "description": "Problemas relacionados à internet.",
                "active": True
            }
        }


models.Base.metadata.create_all(bind=engine)


# @router.get("/categoria/", tags=["Chamado"])
# def get_chamado(db: Session = Depends(get_db)):
#     all_data = db.query(models.Category).all()
#     return{
#         "message": "Dados buscados com sucesso",
#         "error": None,
#         "data": all_data,
#     }


# @router.post("/categoria/", tags=["Chamado"])
# def post_chamado(data: CategoryModel, db: Session = Depends(get_db)):
#     new_object = models.Category(**data.dict())

#     db.add(new_object)
#     db.commit()
#     db.refresh(new_object)
#     return{
#         "message": "Dados buscados com sucesso",
#         "error": None,
#         "data": new_object,
#     }
