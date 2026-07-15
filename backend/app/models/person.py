from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )

    siape: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        unique=True,
        index=True,
    )

    cargo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    setor: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    tipo_vinculo: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="servidor",
    )

    observacoes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ativa: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    contract_assignments: Mapped[list["ContractAssignment"]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan",
    )