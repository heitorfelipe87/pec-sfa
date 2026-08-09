from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PersonBase(BaseModel):
    nome: str = Field(min_length=2, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    siape: str | None = Field(default=None, max_length=20)
    cargo: str | None = Field(default=None, max_length=255)
    setor: str | None = Field(default=None, max_length=100)
    tipo_vinculo: str = Field(default="servidor", max_length=40)
    observacoes: str | None = None
    ativa: bool = True


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    siape: str | None = Field(default=None, max_length=20)
    cargo: str | None = Field(default=None, max_length=255)
    setor: str | None = Field(default=None, max_length=100)
    tipo_vinculo: str | None = Field(default=None, max_length=40)
    observacoes: str | None = None
    ativa: bool | None = None


class PersonRead(PersonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_em: datetime
    atualizado_em: datetime