from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.competence import (
    create_competence,
    get_competence_by_id,
    get_competence_by_period,
    list_competences,
)
from app.repositories.contract import get_contract_by_id
from app.schemas import CompetenceCreate, CompetenceRead


router = APIRouter(
    prefix="/competences",
    tags=["Competências Mensais"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=CompetenceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar competência mensal",
)
def register_competence(
    competence_data: CompetenceCreate,
    database_session: DatabaseSession,
) -> CompetenceRead:
    contract = get_contract_by_id(
        database_session,
        competence_data.contract_id,
    )

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado.",
        )

    existing_competence = get_competence_by_period(
        database_session=database_session,
        contract_id=competence_data.contract_id,
        ano=competence_data.ano,
        mes=competence_data.mes,
    )

    if existing_competence is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Já existe uma competência cadastrada para "
                "este contrato, mês e ano."
            ),
        )

    return create_competence(
        database_session,
        competence_data,
    )


@router.get(
    "",
    response_model=list[CompetenceRead],
    summary="Listar competências mensais",
)
def get_competences(
    database_session: DatabaseSession,
    contract_id: Annotated[
        int | None,
        Query(gt=0),
    ] = None,
    ano: Annotated[
        int | None,
        Query(ge=2000, le=2100),
    ] = None,
    mes: Annotated[
        int | None,
        Query(ge=1, le=12),
    ] = None,
    skip: Annotated[
        int,
        Query(ge=0),
    ] = 0,
    limit: Annotated[
        int,
        Query(ge=1, le=500),
    ] = 100,
) -> list[CompetenceRead]:
    return list_competences(
        database_session=database_session,
        contract_id=contract_id,
        ano=ano,
        mes=mes,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{competence_id}",
    response_model=CompetenceRead,
    summary="Consultar competência mensal",
)
def get_competence(
    competence_id: int,
    database_session: DatabaseSession,
) -> CompetenceRead:
    competence = get_competence_by_id(
        database_session,
        competence_id,
    )

    if competence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Competência não encontrada.",
        )

    return competence