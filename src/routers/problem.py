from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database import engine, SessionLocal
from src.models import Problem, Base
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
                "name": "Internet",
                "description": "Falha ao conectar na internet.",
                "active": True,
                "category_id": 1
            }
        }

models.Base.metadata.create_all(bind=engine)

def get_error_response(e: Exception):
    return {
        "message": "Erro ao processar dados",
        "error": str(e),
        "data": None
    }

@router.get("/problema/", tags=["Chamado"])
async def get_problems(db: Session = Depends(get_db)):
    try:
        all_data = db.query(models.Problem).all()
        all_data = [jsonable_encoder(c) for c in all_data]

        response_data = {
            "message": "Dados buscados com sucesso",
            "error": None,
            "data": all_data,
        }
        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        response_data = {
            "message": "Erro ao buscar dados",
            "error": str(e),
            "data": None
        }
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/problema/{problem_id}", tags=["Problema"])

async def get_problem(problem_id: int = Path(title="The Id of the item to get"), db: Session=Depends(get_db)):
    try:
        problem = await get_problem_from_db(problem_id,db)

        if problem is not None:
            problem = jsonable_encoder(problem)
            message = "Dados buscados com exito"
            status_code = status.HTTP_302_FOUND
        else:
            msg = "Nenhum problema encontrado"
            status_code = status.HTTP_404_NOT_FOUND

        response_data = {
            "message": message,
            "error": None,
            "data": problem,
        }        
        return JSONResponse(content=jsonable_encoder(response_data), status_code= status_code)
    
    except Exception as e:
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/problema/", tags=["Chamado"], response_model=ProblemModel)
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

        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        response_data = jsonable_encoder({
            "message": "Erro ao cadastrar os dados",
            "error": str(e),
            "data": None
        })

        return JSONResponse(content=response_data, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/problema/{problem_id}", tags=["Chamado"])
async def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    try:
        problem = await get_problem_from_db(problem_id, db)
        if problem:
            db.delete(problem)
            db.commit()
            msg = f"Problema de id = {problem_id} deletado com sucesso"

        else:
            msg = f"Problema de id = {problem_id} não encontrado",

        response_data = {
            "message": msg,
            "error": None,
            "data": None,
        }

        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_problem_from_db(problem_id: int, db: Session):
    return db.query(Problem).filter_by(id=problem_id).one_or_none()
