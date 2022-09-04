from datetime import datetime, timedelta
from typing import List, Union

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Category, Problem, Request, alert_date, has

router = APIRouter()


class UpdateHasModel(BaseModel):
    id: int
    problem_id: int | None = None
    category_id: int | None = None
    is_event: bool | None = False
    event_date: str | None = None
    request_status: str | None = "pending"
    priority: str | None = "normal"
    alert_dates: List[str] | None = None
    description: str | None = None


class UpdateRequestModel(BaseModel):
    attendant_name: str | None = None
    applicant_name: str | None = None
    applicant_phone: str | None = None
    created_at: str | None = None
    city_id: int | None = None
    workstation_id: int | None = None
    problems: List[UpdateHasModel] | None = None

    class Config:
        schema_extra = {
            "example": {
                "attendant_name": "John Doe",
                "applicant_name": "Fulano de Tal",
                "applicant_phone": "999999999",
                "city_id": 1,
                "workstation_id": 2,
                "problems": [
                    {
                        "id": 1,
                        "category_id": 1,
                        "problem_id": 2,
                        "is_event": True,
                        "event_date": "2020-02-01T00:00:00",
                        "description": "Chamado sobre acesso a internet.",
                        "request_status": "pending",
                        "priority": "high",
                        "alert_dates": [
                            "2022-01-01T00:00:00",
                            "2022-01-02T00:00:00",
                        ],
                    },
                    {
                        "id": 2,
                        "category_id": 1,
                        "problem_id": 1,
                        "is_event": True,
                        "event_date": "2024-02-01T00:00:00",
                        "description": "Chamado sobre acesso a internet.",
                        "request_status": "pending",
                        "priority": "normal",
                        "alert_dates": [],
                    },
                ],
            }
        }


class hasModel(BaseModel):
    problem_id: int
    category_id: int
    is_event: bool = False
    event_date: str | None = None
    request_status: str = "pending"
    priority: str = "normal"
    alert_dates: List[str] | None = None
    description: str | None = None


class RequestModel(BaseModel):
    attendant_name: str
    applicant_name: str
    applicant_phone: str
    city_id: int
    created_at: str | None = None
    workstation_id: int
    problems: List[hasModel]

    class Config:
        schema_extra = {
            "example": {
                "attendant_name": "Fulano",
                "applicant_name": "Ciclano",
                "applicant_phone": "1111111111",
                "city_id": 1,
                "workstation_id": 1,
                "problems": [
                    {
                        "category_id": 1,
                        "problem_id": 1,
                        "is_event": False,
                        "event_date": None,
                        "request_status": "pending",
                        "description": "Chamado sobre acesso a internet.",
                        "priority": "normal",
                        "alert_dates": None,
                    },
                    {
                        "category_id": 1,
                        "problem_id": 2,
                        "is_event": True,
                        "event_date": "2020-02-01T00:00:00",
                        "description": "Chamado sobre acesso a internet.",
                        "request_status": "pending",
                        "priority": "normal",
                        "alert_dates": [
                            "2020-01-01T00:00:00",
                            "2020-01-02T00:00:00",
                        ],
                    },
                ],
            }
        }


Base.metadata.create_all(bind=engine)


def get_error_response(e: Exception):
    return {
        "message": "Erro ao processar dados",
        "error": str(e),
        "data": None,
    }


@router.post("/chamado", tags=["Chamado"], response_model=RequestModel)
async def post_request(data: RequestModel, db: Session = Depends(get_db)):
    try:
        data_dict = data.dict()
        problems = data_dict.pop("problems")

        new_object = Request(**data_dict)
        db.add(new_object)
        db.commit()
        db.refresh(new_object)
        new_object = jsonable_encoder(new_object)
        for problem in problems:
            problem["request_id"] = new_object["id"]

            alerts = problem.pop("alert_dates")

            result = db.execute(insert(has).values(**problem))

            if alerts:
                for alert in alerts:
                    db.execute(
                        insert(alert_date).values(
                            **{
                                "alert_date": alert,
                                "has_id": result.inserted_primary_key[0],
                            }
                        )
                    )

        db.commit()

        response_data = jsonable_encoder(
            {
                "message": "Dado cadastrado com sucesso",
                "error": None,
                "data": new_object,
            }
        )

        return JSONResponse(
            content=response_data, status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return JSONResponse(
            content=get_error_response(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_has_data(query, db: Session):
    final_list = []
    for request in query:
        request_dict = jsonable_encoder(request)
        requests = (
            db.query(has).filter(has.c.request_id == request_dict["id"]).all()
        )
        lista = []
        for problem in requests:
            problem_data = (
                db.query(Problem).filter_by(id=problem.problem_id).first()
            )
            category_data = (
                db.query(Category).filter_by(id=problem.category_id).first()
            )
            alert_dates = (
                db.query(alert_date)
                .filter(alert_date.c.has_id == problem.id)
                .all()
            )

            alerts_dict = jsonable_encoder(alert_dates)
            problem_dict = jsonable_encoder(problem_data)
            category_dict = jsonable_encoder(category_data)

            tmp_dict = jsonable_encoder(problem)
            tmp_dict["problem"] = problem_dict
            tmp_dict["category"] = category_dict
            tmp_dict["alert_dates"] = [
                date["alert_date"] for date in alerts_dict
            ]
            lista.append(tmp_dict)

        request_dict["problems"] = lista

        final_list.append(request_dict)
    return final_list


@router.get("/evento", tags=["Evento"])
async def get_event(
    days_to_event: Union[int, None] = None, db: Session = Depends(get_db)
):
    try:
        if days_to_event:
            query = (
                db.query(has)
                .filter(
                    has.c.is_event,
                    has.c.event_date >= datetime.now(),
                    has.c.event_date
                    <= datetime.today() + timedelta(days=days_to_event),
                )
                .all()
            )
        else:
            query = (
                db.query(has)
                .filter(has.c.is_event, has.c.event_date >= datetime.today())
                .all()
            )
        final_list = []
        for event in query:
            event_dict = jsonable_encoder(event)
            request = (
                db.query(Request)
                .filter(Request.id == event_dict["request_id"])
                .first()
            )
            request_dict = jsonable_encoder(request)
            request_dict["problems"] = event_dict
            final_list.append(request_dict)

        response_data = jsonable_encoder(
            {
                "message": "Dados recuperados com sucesso",
                "error": None,
                "data": final_list,
            }
        )

        return JSONResponse(
            content=response_data, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content=get_error_response(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/chamado", tags=["Chamado"])
async def get_chamado(
    problem_id: Union[int, None] = None, db: Session = Depends(get_db)
):
    try:
        if problem_id:
            query = (
                db.query(Request)
                .filter(Request.problems.any(id=problem_id))
                .all()
            )

            if query:
                final_list = get_has_data(query, db)
                query = jsonable_encoder(final_list)
                message = "Dados buscados com sucesso"
                status_code = status.HTTP_200_OK
            else:
                message = "Nenhum chamado com esse tipo de problema encontrado"
                status_code = status.HTTP_200_OK

            response_data = {"message": message, "error": None, "data": query}

            return JSONResponse(
                content=jsonable_encoder(response_data),
                status_code=status_code,
            )
        else:
            query = db.query(Request).all()
            all_data = get_has_data(query, db)
            all_data = jsonable_encoder(all_data)
            response_data = {
                "message": "Dados buscados com sucesso",
                "error": None,
                "data": all_data,
            }
            return JSONResponse(
                content=dict(response_data), status_code=status.HTTP_200_OK
            )

    except Exception as e:
        return JSONResponse(
            content=get_error_response(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete("/chamado", tags=["Chamado"])
async def delete_chamado(
    request_id: int, problem_id: int, db: Session = Depends(get_db)
):
    try:
        query = (
            db.query(has)
            .filter(has.c.request_id == request_id)
            .filter(has.c.problem_id == problem_id)
            .update({"request_status": "solved"})
        )

        if query:
            db.commit()
            query_data = (
                db.query(has)
                .filter(has.c.request_id == request_id)
                .filter(has.c.problem_id == problem_id)
                .first()
            )
            query_data = jsonable_encoder(query_data)
            message = "Chamado marcado como resolvido"
        else:
            message = "Chamado não encontrado"
            query_data = None

        response_data = {"message": message, "error": None, "data": query_data}

        return JSONResponse(
            content=response_data, status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return JSONResponse(
            content=get_error_response(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.put("/chamado/{request_id}", tags=["Chamado"])
async def update_chamado(
    data: UpdateRequestModel, request_id: int, db: Session = Depends(get_db)
):
    try:
        query = (
            db.query(Request).filter(Request.id == request_id).one_or_none()
        )
        if query:
            data_dict = data.dict()
            problems = data_dict.pop("problems")
            to_update = (
                db.query(Request)
                .filter(Request.id == request_id)
                .update(data_dict)
            )
            if to_update:
                db.commit()
                for problem in problems:
                    problem = jsonable_encoder(problem)
                    problem_id = problem.pop("id")

                    alerts = problem.pop("alert_dates")
                    problem["request_id"] = request_id
                    print(f" problem = {problem}")

                    has_updated = (
                        db.query(has)
                        .filter(has.c.id == problem_id)
                        .update(problem)
                    )

                    if has_updated:
                        db.commit()
                        db.query(alert_date).filter_by(
                            has_id=problem_id
                        ).delete()
                        db.commit()
                        for alert in alerts:
                            alert = jsonable_encoder(alert)
                            db.execute(
                                insert(alert_date).values(
                                    **{
                                        "alert_date": alert,
                                        "has_id": problem_id,
                                    }
                                )
                            )
                            db.commit()
            query = db.query(Request).filter(Request.id == request_id).all()
            final_list = get_has_data(query, db)
            query = jsonable_encoder(final_list)
            message = "Dados atualizados com sucesso"
            status_code = status.HTTP_200_OK
            response_data = {"message": message, "error": None, "data": query}
        else:
            response_data = {
                "message": "Chamado não encontrado",
                "error": None,
                "data": None,
            }
            status_code = status.HTTP_404_NOT_FOUND
        return JSONResponse(
            content=jsonable_encoder(response_data), status_code=status_code
        )
    except Exception as e:
        return JSONResponse(
            content=get_error_response(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
