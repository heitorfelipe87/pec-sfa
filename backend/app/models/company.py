from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)

    razao_social: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    nome_fantasia: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    cnpj: Mapped[str] = mapped_column(
        String(18),
        nullable=False,
        unique=True,
        index=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    telefone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    representante_legal: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
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

    contracts: Mapped[list["Contract"]] = relationship(
        back_populates="company",
    )