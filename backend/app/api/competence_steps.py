from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.competence import get_competence_by_id
from app.repositories.competence_step import (
    create_competence_step,
    get_competence_step_by_code,
    get_competence_step_by_id,
    list_competence_steps,
    update_competence_step,
)
from app.repositories.person import get_person_by_id
from app.schemas import (
    CompetenceStepCreate,
    CompetenceStepRead,
    CompetenceStepUpdate,
)


router = APIRouter(
    prefix="/competence-steps",
    tags=["Etapas das Competências"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=CompetenceStepRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar etapa da competência",
)
def register_competence_step(
    step_data: CompetenceStepCreate,
    database_session: DatabaseSession,
) -> CompetenceStepRead:
    competence = get_competence_by_id(
        database_session,
        step_data.competence_id,
    )

    if competence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Competência não encontrada.",
        )

    if step_data.responsavel_id is not None:
        person = get_person_by_id(
            database_session,
            step_data.responsavel_id,
        )

        if person is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Responsável não encontrado.",
            )

    existing_step = get_competence_step_by_code(
        database_session=database_session,
        competence_id=step_data.competence_id,
        codigo=step_data.codigo,
    )

    if existing_step is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Esta etapa já foi cadastrada "
                "para a competência informada."
            ),
        )

    return create_competence_step(
        database_session,
        step_data,
    )


@router.get(
    "",
    response_model=list[CompetenceStepRead],
    summary="Listar etapas das competências",
)
def get_competence_steps(
    database_session: DatabaseSession,
    competence_id: Annotated[
        int | None,
        Query(gt=0),
    ] = None,
    situacao: str | None = None,
) -> list[CompetenceStepRead]:
    return list_competence_steps(
        database_session=database_session,
        competence_id=competence_id,
        situacao=situacao,
    )


@router.get(
    "/{step_id}",
    response_model=CompetenceStepRead,
    summary="Consultar etapa da competência",
)
def get_competence_step(
    step_id: int,
    database_session: DatabaseSession,
) -> CompetenceStepRead:
    step = get_competence_step_by_id(
        database_session,
        step_id,
    )

    if step is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Etapa não encontrada.",
        )

    return step


@router.patch(
    "/{step_id}",
    response_model=CompetenceStepRead,
    summary="Atualizar etapa da competência",
)
def patch_competence_step(
    step_id: int,
    step_data: CompetenceStepUpdate,
    database_session: DatabaseSession,
) -> CompetenceStepRead:
    step = get_competence_step_by_id(
        database_session,
        step_id,
    )

    if step is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Etapa não encontrada.",
        )

    if step_data.responsavel_id is not None:
        person = get_person_by_id(
            database_session,
            step_data.responsavel_id,
        )

        if person is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Responsável não encontrado.",
            )

    return update_competence_step(
        database_session,
        step,
        step_data,
    )