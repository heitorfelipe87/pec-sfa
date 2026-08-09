from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.company import (
    create_company,
    get_company_by_cnpj,
    get_company_by_id,
    list_companies,
)
from app.schemas import CompanyCreate, CompanyRead


router = APIRouter(
    prefix="/companies",
    tags=["Empresas"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=CompanyRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar empresa",
)
def register_company(
    company_data: CompanyCreate,
    database_session: DatabaseSession,
) -> CompanyRead:
    existing_company = get_company_by_cnpj(
        database_session,
        company_data.cnpj,
    )

    if existing_company is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma empresa cadastrada com este CNPJ.",
        )

    return create_company(
        database_session,
        company_data,
    )


@router.get(
    "",
    response_model=list[CompanyRead],
    summary="Listar empresas",
)
def get_companies(
    database_session: DatabaseSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> list[CompanyRead]:
    return list_companies(
        database_session,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{company_id}",
    response_model=CompanyRead,
    summary="Consultar empresa",
)
def get_company(
    company_id: int,
    database_session: DatabaseSession,
) -> CompanyRead:
    company = get_company_by_id(
        database_session,
        company_id,
    )

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada.",
        )

    return company