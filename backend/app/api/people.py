from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.person import (
    create_person,
    get_person_by_email,
    get_person_by_id,
    get_person_by_siape,
    list_people,
)
from app.schemas import PersonCreate, PersonRead


router = APIRouter(
    prefix="/people",
    tags=["Pessoas"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=PersonRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar pessoa",
)
def register_person(
    person_data: PersonCreate,
    database_session: DatabaseSession,
) -> PersonRead:
    if person_data.email:
        existing_email = get_person_by_email(
            database_session,
            person_data.email,
        )

        if existing_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma pessoa cadastrada com este e-mail.",
            )

    if person_data.siape:
        existing_siape = get_person_by_siape(
            database_session,
            person_data.siape,
        )

        if existing_siape is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma pessoa cadastrada com este SIAPE.",
            )

    return create_person(
        database_session,
        person_data,
    )


@router.get(
    "",
    response_model=list[PersonRead],
    summary="Listar pessoas",
)
def get_people(
    database_session: DatabaseSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> list[PersonRead]:
    return list_people(
        database_session,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{person_id}",
    response_model=PersonRead,
    summary="Consultar pessoa",
)
def get_person(
    person_id: int,
    database_session: DatabaseSession,
) -> PersonRead:
    person = get_person_by_id(
        database_session,
        person_id,
    )

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada.",
        )

    return person
