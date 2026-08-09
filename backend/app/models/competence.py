from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Competence(Base):
    __tablename__ = "competences"

    __table_args__ = (
        UniqueConstraint(
            "contract_id",
            "ano",
            "mes",
            name="uq_competence_contract_year_month",
        ),
        CheckConstraint(
            "mes >= 1 AND mes <= 12",
            name="ck_competence_valid_month",
        ),
        CheckConstraint(
            "ano >= 2000 AND ano <= 2100",
            name="ck_competence_valid_year",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ano: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    mes: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    valor_previsto: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2),
        nullable=True,
    )

    valor_faturado: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2),
        nullable=True,
    )

    situacao: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="nao_iniciada",
        index=True,
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

    contract: Mapped["Contract"] = relationship(
        back_populates="competences",
    )

    steps: Mapped[list["CompetenceStep"]] = relationship(
        back_populates="competence",
        cascade="all, delete-orphan",
        order_by="CompetenceStep.ordem",
    )  