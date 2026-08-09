from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContractBase(BaseModel):
    company_id: int
    numero: str = Field(min_length=1, max_length=30)

    processo_sei_contratacao: str = Field(min_length=1, max_length=30)
    processo_sei_fiscalizacao: str | None = Field(default=None, max_length=30)
    processo_sei_pagamento: str | None = Field(default=None, max_length=30)

    objeto: str = Field(min_length=3)

    valor_global: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    valor_mensal: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=14,
        decimal_places=2,
    )

    data_inicio: date
    data_fim: date

    situacao: str = Field(default="vigente", max_length=30)
    observacoes: str | None = None

    @model_validator(mode="after")
    def validar_periodo(self):
        if self.data_fim < self.data_inicio:
            raise ValueError(
                "A data final não pode ser anterior à data inicial."
            )

        return self


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    company_id: int | None = None
    numero: str | None = Field(default=None, min_length=1, max_length=30)

    processo_sei_contratacao: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )
    processo_sei_fiscalizacao: str | None = Field(default=None, max_length=30)
    processo_sei_pagamento: str | None = Field(default=None, max_length=30)

    objeto: str | None = Field(default=None, min_length=3)

    valor_global: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=14,
        decimal_places=2,
    )
    valor_mensal: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=14,
        decimal_places=2,
    )

    data_inicio: date | None = None
    data_fim: date | None = None

    situacao: str | None = Field(default=None, max_length=30)
    observacoes: str | None = None


class ContractRead(ContractBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_em: datetime
    atualizado_em: datetime