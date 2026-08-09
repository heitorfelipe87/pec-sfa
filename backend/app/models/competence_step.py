from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class CompetenceStep(Base):
    __tablename__ = "competence_steps"

    __table_args__ = (
        UniqueConstraint(
            "competence_id",
            "codigo",
            name="uq_competence_step_code",
        ),
        CheckConstraint(
            "ordem > 0",
            name="ck_competence_step_positive_order",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    competence_id: Mapped[int] = mapped_column(
        ForeignKey("competences.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    codigo: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
        index=True,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    ordem: Mapped[int] = mapped_column(
        nullable=False,
    )

    situacao: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pendente",
        index=True,
    )

    responsavel_id: Mapped[int | None] = mapped_column(
        ForeignKey("people.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    data_prevista: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    concluida_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    numero_sei_documento: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    observacoes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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

    competence: Mapped["Competence"] = relationship(
        back_populates="steps",
    )

    responsavel: Mapped["Person | None"] = relationship()