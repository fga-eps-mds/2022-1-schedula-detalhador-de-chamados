
from typing import Union

from fastapi import APIRouter, Depends, Path, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Category

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
    active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "name": "Internet",
                "description": "Problemas relacionados à internet.",
            }
        }


Base.metadata.create_all(bind=engine)


def get_error_response(e: Exception):
    return {
        "message": "Erro ao processar dados",
        "error": str(e),
        "data": None
    }


@router.post("/categoria/", tags=["Categoria"], response_model=CategoryModel)
async def post_category(data: CategoryModel, db: Session = Depends(get_db)):
    try:
        new_object = Category(**data.dict())
        db.add(new_object)
        db.commit()
        db.refresh(new_object)
        new_object = jsonable_encoder(new_object)
        response_data = jsonable_encoder({
            "message": "Dado cadastrado com sucesso",
            "error": None,
            "data": new_object
        })

        return JSONResponse(
            content=response_data,
            status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(content=get_error_response(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/categoria/", tags=["Categoria"])
async def get_categories(
        category_id: Union[int, None] = None,
        db: Session = Depends(get_db)
):
    try:
        if category_id:
            category = db.query(Category).filter_by(id=category_id).all()

            if category is not None:
                category = jsonable_encoder(category)
                message = "Dados buscados com sucesso"
                status_code = status.HTTP_200_OK
            else:
                message = "Nenhuma categoria encontrada"
                status_code = status.HTTP_200_OK

            response_data = {
                "message": message,
                "error": None,
                "data": category,
            }

            return JSONResponse(
                content=jsonable_encoder(response_data),
                status_code=status_code)
        else:
            all_data = db.query(Category).filter_by(active=True).all()
            all_data = [jsonable_encoder(c) for c in all_data]
            response_data = {
                "message": "Dados buscados com sucesso",
                "error": None,
                "data": all_data,
            }
            return JSONResponse(
                content=dict(response_data),
                status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content=get_error_response(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/categoria/{category_id}", tags=["Categoria"])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category = db.query(Category).filter_by(id=category_id).one_or_none()
        if category:
            category.active = False
            db.commit()
            message = f"Categoria de id = {category_id} deletada com sucesso"

        else:
            message = f"Categoria de id = {category_id} não encontrada"

        response_data = {
            "message": message,
            "error": None,
            "data": None,
        }

        return JSONResponse(
            content=response_data,
            status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content=get_error_response(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/categoria/{category_id}", tags=["Categoria"])
async def update_category(
        data: CategoryModel,
        category_id: int = Path(title="The ID of the item to update"),
        db: Session = Depends(get_db)
):
    try:
        db.query(Category).filter_by(id=category_id).update(data.dict())
        db.commit()

        # data = jsonable_encoder(category)
        response_data = jsonable_encoder({
            "message": "Dado atualizado com sucesso",
            "error": None,
            "data": None
        })

        return JSONResponse(
            content=response_data,
            status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content=get_error_response(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
