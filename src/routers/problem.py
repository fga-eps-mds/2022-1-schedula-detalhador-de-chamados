from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.params import Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import engine, get_db
from src.models import Base, Problem

router = APIRouter()


class ProblemModel(BaseModel):
    name: str
    description: str
    active: bool = True
    category_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Internet",
                "description": "Falha ao conectar na internet.",
                "category_id": 1
            }
        }


Base.metadata.create_all(bind=engine)


def get_error_response(e: Exception):
    return {
        "message": "Erro ao processar dados",
        "error": str(e),
        "data": None
    }


@router.get("/problema/", tags=["Problema"])
async def get_problems(
        problem_id: Union[int, None] = None,
        db: Session = Depends(get_db)
):
    try:
        if problem_id:
            problem = db.query(Problem).filter_by(id=problem_id).one_or_none()
            if problem:
                problem = jsonable_encoder(problem)
                message = "Dados buscados com exito"
                status_code = status.HTTP_200_OK
            else:
                message = "Nenhum problema encontrado"
                status_code = status.HTTP_200_OK

            response_data = {
                "message": message,
                "error": None,
                "data": problem,
            }
            return JSONResponse(
                content=jsonable_encoder(response_data),
                status_code=status_code)

        else:
            all_data = db.query(Problem).filter_by(active=True).all()
            all_data = [jsonable_encoder(c) for c in all_data]

            response_data = {
                "message": "Dados buscados com sucesso",
                "error": None,
                "data": all_data,
            }
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_201_CREATED)
    except Exception as e:
        response_data = {
            "message": "Erro ao buscar dados",
            "error": str(e),
            "data": None
        }
        return JSONResponse(content=get_error_response(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/problema/{problem_id}", tags=["Problema"])
async def get_problem(problem_id: int = Path(title="The ID of the item to get"), db: Session = Depends(get_db)):
    try:
        problem = db.query(Problem).filter_by(id=problem_id).one_or_none()
        if problem is not None:
            problem = jsonable_encoder(problem)
            msg = "Dados buscados com sucesso"
            status_code = status.HTTP_302_FOUND
        else:
            msg = "Nenhum problema encontrado"
            status_code = status.HTTP_404_NOT_FOUND

        response_data = {
            "message": msg,
            "error": None,
            "data": problem,
        }
        return JSONResponse(content=jsonable_encoder(response_data), status_code=status_code)
    except Exception as e:
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/problema/", tags=["Problema"], response_model=ProblemModel)
async def post_problem(data: ProblemModel, db: Session = Depends(get_db)):
    try:
        problem = Problem(**data.dict())

        db.add(problem)
        db.commit()
        db.refresh(problem)
        problem = jsonable_encoder(problem)
        response_data = jsonable_encoder({
            "message": "Dados cadastrados com sucesso",
            "error": None,
            "data": problem
        })

        return JSONResponse(
            content=response_data,
            status_code=status.HTTP_201_CREATED)
    except Exception as e:
        response_data = jsonable_encoder({
            "message": "Erro ao cadastrar os dados",
            "error": str(e),
            "data": None
        })

        return JSONResponse(content=response_data,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/problema/{problem_id}", tags=["Problema"])
async def update_problem(data: ProblemModel, problem_id: int = Path(title="The ID of the item to update"),
                         db: Session = Depends(get_db)):
    try:
        input_values = Problem(**data.dict())
        print(problem_id)
        problem = db.query(Problem).filter_by(id=problem_id).one_or_none()
        print(jsonable_encoder(problem))
        if problem:
            problem.name = input_values.name
            problem.description = input_values.description
            problem.active = input_values.active

            db.add(problem)
            db.commit()
            db.refresh(problem)

            problem = jsonable_encoder(problem)
            response_data = jsonable_encoder({
                "message": "Dado atualizado com sucesso",
                "error": None,
                "data": problem
            })
        else:
            response_data = jsonable_encoder({
                "message": f"Problema de id = {problem_id} não encontrado",
                "error": None,
                "data": None
            })

        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/problema/{problem_id}", tags=["Problema"])
async def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    try:
        problem = db.query(Problem).filter_by(id=problem_id).one_or_none()
        if problem:
            problem.active = False
            db.commit()
            msg = f"Problema de id = {problem_id} deletado com sucesso"

        else:
            msg = f"Problema de id = {problem_id} não encontrado",

        response_data = {
            "message": msg,
            "error": None,
            "data": None,
        }

        return JSONResponse(
            content=response_data,
            status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content=get_error_response(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
