from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.contract import get_contract_by_id
from app.repositories.contract_assignment import (
    create_contract_assignment,
    get_contract_assignment_by_id,
    get_matching_contract_assignment,
    list_contract_assignments,
)
from app.repositories.person import get_person_by_id
from app.schemas import (
    ContractAssignmentCreate,
    ContractAssignmentRead,
)


router = APIRouter(
    prefix="/contract-assignments",
    tags=["Equipe dos Contratos"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=ContractAssignmentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Vincular pessoa ao contrato",
)
def register_contract_assignment(
    assignment_data: ContractAssignmentCreate,
    database_session: DatabaseSession,
) -> ContractAssignmentRead:
    contract = get_contract_by_id(
        database_session,
        assignment_data.contract_id,
    )

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado.",
        )

    person = get_person_by_id(
        database_session,
        assignment_data.person_id,
    )

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada.",
        )

    existing_assignment = get_matching_contract_assignment(
        database_session=database_session,
        contract_id=assignment_data.contract_id,
        person_id=assignment_data.person_id,
        role=assignment_data.role,
        data_inicio=assignment_data.data_inicio,
    )

    if existing_assignment is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Esta pessoa já possui essa designação no contrato "
                "com a mesma data inicial."
            ),
        )

    return create_contract_assignment(
        database_session,
        assignment_data,
    )


@router.get(
    "",
    response_model=list[ContractAssignmentRead],
    summary="Listar designações da equipe",
)
def get_contract_assignments(
    database_session: DatabaseSession,
    contract_id: Annotated[
        int | None,
        Query(gt=0),
    ] = None,
    person_id: Annotated[
        int | None,
        Query(gt=0),
    ] = None,
) -> list[ContractAssignmentRead]:
    return list_contract_assignments(
        database_session=database_session,
        contract_id=contract_id,
        person_id=person_id,
    )


@router.get(
    "/{assignment_id}",
    response_model=ContractAssignmentRead,
    summary="Consultar designação",
)
def get_contract_assignment(
    assignment_id: int,
    database_session: DatabaseSession,
) -> ContractAssignmentRead:
    assignment = get_contract_assignment_by_id(
        database_session,
        assignment_id,
    )

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Designação não encontrada.",
        )

    return assignment