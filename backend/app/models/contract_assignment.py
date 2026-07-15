from datetime import date, datetime

from sqlalchemy import (
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


class ContractAssignment(Base):
    __tablename__ = "contract_assignments"

    __table_args__ = (
        UniqueConstraint(
            "contract_id",
            "person_id",
            "role",
            "data_inicio",
            name="uq_contract_assignment",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    titular: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )

    data_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    data_fim: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    documento_designacao: Mapped[str | None] = mapped_column(
        String(100),
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

    contract: Mapped["Contract"] = relationship(
        back_populates="assignments",
    )

    person: Mapped["Person"] = relationship(
        back_populates="contract_assignments",
    )