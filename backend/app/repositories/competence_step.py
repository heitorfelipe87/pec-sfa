from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CompetenceStep
from app.schemas import (
    CompetenceStepCreate,
    CompetenceStepUpdate,
)


def get_competence_step_by_id(
    database_session: Session,
    step_id: int,
) -> CompetenceStep | None:
    return database_session.get(
        CompetenceStep,
        step_id,
    )


def get_competence_step_by_code(
    database_session: Session,
    competence_id: int,
    codigo: str,
) -> CompetenceStep | None:
    statement = select(CompetenceStep).where(
        CompetenceStep.competence_id == competence_id,
        CompetenceStep.codigo == codigo,
    )

    return database_session.scalar(statement)


def list_competence_steps(
    database_session: Session,
    competence_id: int | None = None,
    situacao: str | None = None,
) -> list[CompetenceStep]:
    statement = select(CompetenceStep)

    if competence_id is not None:
        statement = statement.where(
            CompetenceStep.competence_id == competence_id,
        )

    if situacao is not None:
        statement = statement.where(
            CompetenceStep.situacao == situacao,
        )

    statement = statement.order_by(
        CompetenceStep.competence_id,
        CompetenceStep.ordem,
    )

    return list(database_session.scalars(statement).all())


def create_competence_step(
    database_session: Session,
    step_data: CompetenceStepCreate,
) -> CompetenceStep:
    step = CompetenceStep(
        **step_data.model_dump()
    )

    database_session.add(step)
    database_session.commit()
    database_session.refresh(step)

    return step


def update_competence_step(
    database_session: Session,
    step: CompetenceStep,
    step_data: CompetenceStepUpdate,
) -> CompetenceStep:
    update_data = step_data.model_dump(
        exclude_unset=True,
    )

    if update_data.get("situacao") == "concluida":
        if "concluida_em" not in update_data:
            update_data["concluida_em"] = datetime.now(
                timezone.utc
            )

    if (
        "situacao" in update_data
        and update_data["situacao"] != "concluida"
        and "concluida_em" not in update_data
    ):
        update_data["concluida_em"] = None

    for field_name, value in update_data.items():
        setattr(step, field_name, value)

    database_session.commit()
    database_session.refresh(step)

    return step