from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database import engine, SessionLocal
import src.models as models


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProblemModel(BaseModel):
    name: str
    description: str
    active: bool
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


# @router.get("/problema/", tags=["Chamado"])
# def get_problem(db: Session = Depends(get_db)):
#     try:
#         all_data = db.query(models.Problem).all()
#         response_data = {
#             "message": "Dados buscados com sucesso",
#             "error": None,
#             "data": all_data,
#         }
#         return Response(content=response_data, status_code=status.HTTP_201_CREATED)
#     except Exception as e:
#         response_data = {
#             "message": "Erro ao buscar dados",
#             "error": str(e),
#             "data": None
#         }
#         return Response(content=response_data, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/problema/", tags=["Chamado"], response_model=ProblemModel)
def post_problem(data: ProblemModel, db: Session = Depends(get_db)):
    try:
        new_object = models.Problem(**data.dict())
        db.add(new_object)

        db.commit()
        db.refresh(new_object)
        new_object = jsonable_encoder(new_object)
        response_data = jsonable_encoder({
            "message": "Dados cadastrados com sucesso",
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