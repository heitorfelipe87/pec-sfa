from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Contract
from app.schemas import ContractCreate


def get_contract_by_id(
    database_session: Session,
    contract_id: int,
) -> Contract | None:
    return database_session.get(Contract, contract_id)


def list_contracts(
    database_session: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Contract]:
    statement = (
        select(Contract)
        .order_by(
            Contract.data_fim,
            Contract.numero,
        )
        .offset(skip)
        .limit(limit)
    )

    return list(database_session.scalars(statement).all())


def create_contract(
    database_session: Session,
    contract_data: ContractCreate,
) -> Contract:
    contract = Contract(**contract_data.model_dump())

    database_session.add(contract)
    database_session.commit()
    database_session.refresh(contract)

    return contract