
from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from src.database import engine, SessionLocal
from src.models import Category, Base
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

        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/categoria/", tags=["Categoria"])
async def get_categories(db: Session = Depends(get_db)):
    try:
        all_data = db.query(Category).all()
        all_data = [jsonable_encoder(c) for c in all_data]
        response_data = {
            "message": "Dados buscados com sucesso",
            "error": None,
            "data": all_data,
        }
        return JSONResponse(content=dict(response_data), status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/categoria/{category_id}", tags=["Categoria"])
async def get_category(category_id: int = Path(title="The ID of the item to get"), db: Session = Depends(get_db)):
    try:
        category = await get_category_from_db(category_id, db)

        if category is not None:
            category = jsonable_encoder(category)
            msg = "Dados buscados com sucesso"
            status_code = status.HTTP_302_FOUND
        else:
            msg = "Nenhuma categoria encontrada"
            status_code = status.HTTP_404_NOT_FOUND

        response_data = {
            "message": msg,
            "error": None,
            "data": category,
        }

        return JSONResponse(content=jsonable_encoder(response_data), status_code=status_code)

    except Exception as e:
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/categoria/{category_id}", tags=["Categoria"])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category = await get_category_from_db(category_id, db)
        if category:
            category.active = False
            await update_category_on_db(category_id, category, db)
            # db.delete(category)
            db.commit()
            msg = f"Categoria de id = {category_id} deletada com sucesso"

        else:
            msg = f"Categoria de id = {category_id} não encontrada",

        response_data = {
            "message": msg,
            "error": None,
            "data": None,
        }

        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/categoria/{category_id}", tags=["Categoria"])
async def update_category(data: CategoryModel, category_id: int = Path(title="The ID of the item to update"), db: Session = Depends(get_db)):
    try:
        input_values = Category(**data.dict())
        category = await update_category_on_db(category_id, input_values, db)
        if category:
            category = jsonable_encoder(category)
            response_data = jsonable_encoder({
                "message": "Dado atualizado com sucesso",
                "error": None,
                "data": category
            })
        else:
            response_data = jsonable_encoder({
                "message": f"Categoria de id = {category_id} não encontrada",
                "error": None,
                "data": None
            })

        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(content=get_error_response(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_category_from_db(category_id: int, db: Session):
    return db.query(Category).filter_by(id=category_id).one_or_none()


async def update_category_on_db(category_id: int, input_values: Category, db: Session):

    category = await get_category_from_db(category_id, db)
    if category:
        category.name = input_values.name
        category.description = input_values.description
        category.active = input_values.active

        db.add(category)
        db.commit()
        db.refresh(category)

    return category
