from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.competence_workflow import DEFAULT_COMPETENCE_STEPS
from app.models import Competence, CompetenceStep
from app.schemas import CompetenceCreate


def get_competence_by_id(
    database_session: Session,
    competence_id: int,
) -> Competence | None:
    return database_session.get(
        Competence,
        competence_id,
    )


def get_competence_by_period(
    database_session: Session,
    contract_id: int,
    ano: int,
    mes: int,
) -> Competence | None:
    statement = select(Competence).where(
        Competence.contract_id == contract_id,
        Competence.ano == ano,
        Competence.mes == mes,
    )

    return database_session.scalar(statement)


def list_competences(
    database_session: Session,
    contract_id: int | None = None,
    ano: int | None = None,
    mes: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Competence]:
    statement = select(Competence)

    if contract_id is not None:
        statement = statement.where(
            Competence.contract_id == contract_id,
        )

    if ano is not None:
        statement = statement.where(
            Competence.ano == ano,
        )

    if mes is not None:
        statement = statement.where(
            Competence.mes == mes,
        )

    statement = (
        statement
        .order_by(
            Competence.ano.desc(),
            Competence.mes.desc(),
            Competence.contract_id,
        )
        .offset(skip)
        .limit(limit)
    )

    return list(database_session.scalars(statement).all())


def create_competence(
    database_session: Session,
    competence_data: CompetenceCreate,
) -> Competence:
    competence = Competence(
        **competence_data.model_dump()
    )

    database_session.add(competence)

    # Obtém o ID da competência antes do commit.
    database_session.flush()

    for step_template in DEFAULT_COMPETENCE_STEPS:
        step = CompetenceStep(
            competence_id=competence.id,
            codigo=step_template["codigo"],
            nome=step_template["nome"],
            ordem=step_template["ordem"],
            situacao="pendente",
        )

        database_session.add(step)

    database_session.commit()
    database_session.refresh(competence)

    return competence