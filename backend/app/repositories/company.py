from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Company
from app.schemas import CompanyCreate


def get_company_by_id(
    database_session: Session,
    company_id: int,
) -> Company | None:
    return database_session.get(Company, company_id)


def get_company_by_cnpj(
    database_session: Session,
    cnpj: str,
) -> Company | None:
    statement = select(Company).where(Company.cnpj == cnpj)

    return database_session.scalar(statement)


def list_companies(
    database_session: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Company]:
    statement = (
        select(Company)
        .order_by(Company.razao_social)
        .offset(skip)
        .limit(limit)
    )

    return list(database_session.scalars(statement).all())


def create_company(
    database_session: Session,
    company_data: CompanyCreate,
) -> Company:
    company = Company(**company_data.model_dump())

    database_session.add(company)
    database_session.commit()
    database_session.refresh(company)

    return company