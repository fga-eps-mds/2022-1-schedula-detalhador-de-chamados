
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from src.database import engine, SessionLocal
import src.models as models
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CategoryModel(BaseModel):
    name: str
    description: str
    active: bool

    class Config:
        schema_extra = {
            "example": {
                "name": "Internet",
                "description": "Problemas relacionados à internet.",
                "active": True
            }
        }


models.Base.metadata.create_all(bind=engine)


@router.post("/categoria/", tags=["Chamado"], response_model=CategoryModel)
def post_category(data: CategoryModel, db: Session = Depends(get_db)):
    try:
        new_object = models.Category(**data.dict())
        db.add(new_object)
        db.commit()
        db.refresh(new_object)
        new_object = jsonable_encoder(new_object)
        response_data = jsonable_encoder({
            "message": "Dado cadastrado com sucesso",
            "error": None,
            "data": new_object
        })

        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        response_data = jsonable_encoder({
            "message": "Erro ao cadastrar os dados",
            "error": str(e),
            "data": None
        })
        return JSONResponse(content=response_data, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @router.get("/categoria/", tags=["Chamado"])
# def get_category(db: Session = Depends(get_db)):
#     try:
#         all_data = db.query(models.Category).all()
#         response_data = {
#             "message": "Dados buscados com sucesso",
#             "error": None,
#             "data": all_data,
#         }
#         return JSONResponse(content=dict(response_data), status_code=status.HTTP_201_CREATED)

#     except Exception as e:
#         response_data = {
#             "message": "Erro ao buscar dados",
#             "error": str(e),
#             "data": None
#         }
#         return JSONResponse(content=response_data, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
