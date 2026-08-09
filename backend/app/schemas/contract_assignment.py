from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


ContractRole = Literal[
    "gestor",
    "gestor_substituto",
    "fiscal_tecnico",
    "fiscal_tecnico_substituto",
    "fiscal_administrativo",
    "fiscal_administrativo_substituto",
]


class ContractAssignmentBase(BaseModel):
    contract_id: int = Field(gt=0)
    person_id: int = Field(gt=0)

    role: ContractRole
    titular: bool = True

    data_inicio: date
    data_fim: date | None = None

    documento_designacao: str | None = Field(
        default=None,
        max_length=100,
    )
    numero_sei_documento: str | None = Field(
        default=None,
        max_length=30,
    )
    observacoes: str | None = None

    @model_validator(mode="after")
    def validar_periodo(self):
        if self.data_fim is not None and self.data_fim < self.data_inicio:
            raise ValueError(
                "A data final da designação não pode ser anterior à data inicial."
            )

        return self


class ContractAssignmentCreate(ContractAssignmentBase):
    pass


class ContractAssignmentUpdate(BaseModel):
    role: ContractRole | None = None
    titular: bool | None = None
    data_inicio: date | None = None
    data_fim: date | None = None
    documento_designacao: str | None = Field(
        default=None,
        max_length=100,
    )
    numero_sei_documento: str | None = Field(
        default=None,
        max_length=30,
    )
    observacoes: str | None = None


class ContractAssignmentRead(ContractAssignmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_em: datetime