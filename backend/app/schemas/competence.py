from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CompetenceStatus = Literal[
    "nao_iniciada",
    "em_fiscalizacao",
    "aguardando_empresa",
    "aguardando_nota_fiscal",
    "aguardando_atesto",
    "aguardando_termo_definitivo",
    "em_analise_cad",
    "aguardando_autorizacao",
    "em_pagamento",
    "paga",
    "suspensa",
]


class CompetenceBase(BaseModel):
    contract_id: int = Field(gt=0)

    ano: int = Field(ge=2000, le=2100)
    mes: int = Field(ge=1, le=12)

    valor_previsto: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=14,
        decimal_places=2,
    )

    valor_faturado: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=14,
        decimal_places=2,
    )

    situacao: CompetenceStatus = "nao_iniciada"
    observacoes: str | None = None


class CompetenceCreate(CompetenceBase):
    pass


class CompetenceUpdate(BaseModel):
    valor_previsto: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=14,
        decimal_places=2,
    )

    valor_faturado: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=14,
        decimal_places=2,
    )

    situacao: CompetenceStatus | None = None
    observacoes: str | None = None


class CompetenceRead(CompetenceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_em: datetime
    atualizado_em: datetime