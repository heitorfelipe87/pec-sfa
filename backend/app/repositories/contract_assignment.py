from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ContractAssignment
from app.schemas import ContractAssignmentCreate


def get_contract_assignment_by_id(
    database_session: Session,
    assignment_id: int,
) -> ContractAssignment | None:
    return database_session.get(
        ContractAssignment,
        assignment_id,
    )


def get_matching_contract_assignment(
    database_session: Session,
    contract_id: int,
    person_id: int,
    role: str,
    data_inicio: date,
) -> ContractAssignment | None:
    statement = select(ContractAssignment).where(
        ContractAssignment.contract_id == contract_id,
        ContractAssignment.person_id == person_id,
        ContractAssignment.role == role,
        ContractAssignment.data_inicio == data_inicio,
    )

    return database_session.scalar(statement)


def list_contract_assignments(
    database_session: Session,
    contract_id: int | None = None,
    person_id: int | None = None,
) -> list[ContractAssignment]:
    statement = select(ContractAssignment)

    if contract_id is not None:
        statement = statement.where(
            ContractAssignment.contract_id == contract_id,
        )

    if person_id is not None:
        statement = statement.where(
            ContractAssignment.person_id == person_id,
        )

    statement = statement.order_by(
        ContractAssignment.contract_id,
        ContractAssignment.role,
        ContractAssignment.data_inicio.desc(),
    )

    return list(database_session.scalars(statement).all())


def create_contract_assignment(
    database_session: Session,
    assignment_data: ContractAssignmentCreate,
) -> ContractAssignment:
    assignment = ContractAssignment(
        **assignment_data.model_dump()
    )

    database_session.add(assignment)
    database_session.commit()
    database_session.refresh(assignment)

    return assignment