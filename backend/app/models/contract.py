from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    numero: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    processo_sei_contratacao: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    processo_sei_fiscalizacao: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        index=True,
    )

    processo_sei_pagamento: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        index=True,
    )

    objeto: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    valor_global: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    valor_mensal: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2),
        nullable=True,
    )

    data_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    data_fim: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    situacao: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="vigente",
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

    company: Mapped["Company"] = relationship(
        back_populates="contracts",
    )

    assignments: Mapped[list["ContractAssignment"]] = relationship(
        back_populates="contract",
        cascade="all, delete-orphan",
    )