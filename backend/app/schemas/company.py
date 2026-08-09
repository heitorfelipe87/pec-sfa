from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CompanyBase(BaseModel):
    razao_social: str = Field(min_length=2, max_length=255)
    nome_fantasia: str | None = Field(default=None, max_length=255)
    cnpj: str = Field(min_length=14, max_length=18)
    email: str | None = Field(default=None, max_length=255)
    telefone: str | None = Field(default=None, max_length=30)
    representante_legal: str | None = Field(default=None, max_length=255)
    observacoes: str | None = None
    ativa: bool = True


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    razao_social: str | None = Field(default=None, min_length=2, max_length=255)
    nome_fantasia: str | None = Field(default=None, max_length=255)
    cnpj: str | None = Field(default=None, min_length=14, max_length=18)
    email: str | None = Field(default=None, max_length=255)
    telefone: str | None = Field(default=None, max_length=30)
    representante_legal: str | None = Field(default=None, max_length=255)
    observacoes: str | None = None
    ativa: bool | None = None


class CompanyRead(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_em: datetime
    atualizado_em: datetime