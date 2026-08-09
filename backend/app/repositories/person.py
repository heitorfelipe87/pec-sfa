from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Person
from app.schemas import PersonCreate


def get_person_by_id(
    database_session: Session,
    person_id: int,
) -> Person | None:
    return database_session.get(Person, person_id)


def get_person_by_email(
    database_session: Session,
    email: str,
) -> Person | None:
    statement = select(Person).where(Person.email == email)

    return database_session.scalar(statement)


def get_person_by_siape(
    database_session: Session,
    siape: str,
) -> Person | None:
    statement = select(Person).where(Person.siape == siape)

    return database_session.scalar(statement)


def list_people(
    database_session: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Person]:
    statement = (
        select(Person)
        .order_by(Person.nome)
        .offset(skip)
        .limit(limit)
    )

    return list(database_session.scalars(statement).all())


def create_person(
    database_session: Session,
    person_data: PersonCreate,
) -> Person:
    person = Person(**person_data.model_dump())

    database_session.add(person)
    database_session.commit()
    database_session.refresh(person)

    return person