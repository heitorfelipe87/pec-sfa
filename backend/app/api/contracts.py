from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.company import get_company_by_id
from app.repositories.contract import (
    create_contract,
    get_contract_by_id,
    list_contracts,
)
from app.schemas import ContractCreate, ContractRead


router = APIRouter(
    prefix="/contracts",
    tags=["Contratos"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=ContractRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar contrato",
)
def register_contract(
    contract_data: ContractCreate,
    database_session: DatabaseSession,
) -> ContractRead:
    company = get_company_by_id(
        database_session,
        contract_data.company_id,
    )

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A empresa informada não foi encontrada.",
        )

    return create_contract(
        database_session,
        contract_data,
    )


@router.get(
    "",
    response_model=list[ContractRead],
    summary="Listar contratos",
)
def get_contracts(
    database_session: DatabaseSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> list[ContractRead]:
    return list_contracts(
        database_session,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{contract_id}",
    response_model=ContractRead,
    summary="Consultar contrato",
)
def get_contract(
    contract_id: int,
    database_session: DatabaseSession,
) -> ContractRead:
    contract = get_contract_by_id(
        database_session,
        contract_id,
    )

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado.",
        )

    return contract