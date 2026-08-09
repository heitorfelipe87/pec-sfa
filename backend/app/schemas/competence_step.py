from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CompetenceStepCode = Literal[
    "documentacao_administrativa",
    "relatorio_fiscalizacao",
    "imr_elaborado",
    "imr_assinado_fiscal",
    "imr_assinado_empresa",
    "emissao_nf_autorizada",
    "nota_fiscal_emitida",
    "nota_fiscal_atestada",
    "termo_recebimento_definitivo",
    "encaminhado_cad",
    "despacho_cad",
    "pagamento_autorizado",
    "liquidacao",
    "pagamento",
    "ordem_bancaria_anexada",
]

CompetenceStepStatus = Literal[
    "pendente",
    "em_andamento",
    "concluida",
    "nao_aplicavel",
]


class CompetenceStepBase(BaseModel):
    competence_id: int = Field(gt=0)
    codigo: CompetenceStepCode
    nome: str = Field(min_length=2, max_length=150)
    ordem: int = Field(gt=0)

    situacao: CompetenceStepStatus = "pendente"
    responsavel_id: int | None = Field(default=None, gt=0)
    data_prevista: date | None = None
    concluida_em: datetime | None = None

    numero_sei_documento: str | None = Field(
        default=None,
        max_length=30,
    )

    observacoes: str | None = None


class CompetenceStepCreate(CompetenceStepBase):
    pass


class CompetenceStepUpdate(BaseModel):
    situacao: CompetenceStepStatus | None = None
    responsavel_id: int | None = Field(default=None, gt=0)
    data_prevista: date | None = None
    concluida_em: datetime | None = None

    numero_sei_documento: str | None = Field(
        default=None,
        max_length=30,
    )

    observacoes: str | None = None


class CompetenceStepRead(CompetenceStepBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_em: datetime
    atualizado_em: datetime