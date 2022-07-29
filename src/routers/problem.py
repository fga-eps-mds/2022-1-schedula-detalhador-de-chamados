# import json
#
# from fastapi import APIRouter, Depends, status
# from fastapi.openapi.models import Response
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
#
# from src.database import engine, SessionLocal
# import src.models as models
#
# router = APIRouter()
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# class ProblemModel(BaseModel):
#     name: str
#     description: str
#     active: bool
#     category_id: int
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Falha na conexão com a internet.",
#                 "description": "Falha ao conectar na internet.",
#                 "active": True,
#                 "category_id": 1
#             }
#         }
#
#
# models.Base.metadata.create_all(bind=engine)
#
#
# @router.get("/chamado/", tags=["Chamado"])
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
#
#
# @router.post("/chamado/", tags=["Chamado"])
# def post_chamado(data: ProblemModel, db: Session = Depends(get_db)):
#     try:
#         new_object = models.Problem(**data.dict())
#         db.add(new_object)
#
#         db.commit()
#         db.refresh(new_object)
#         new_object = json.loads(json.dumps(new_object))
#         return {
#             "message": "Dados buscados com sucesso",
#             "error": None,
#             "data": new_object,
#         }
#     except Exception as e:
#         response_data = {
#             "message": "Erro ao buscar dados",
#             "error": str(e),
#             "data": None
#         }
#         return Response(content=response_data, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
