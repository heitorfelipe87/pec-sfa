from fastapi import FastAPI

from app.api import (
    companies_router,
    competences_router,
    competence_steps_router,
    contract_assignments_router,
    contracts_router,
    people_router,
)


app = FastAPI(
    title="PEC-SFA",
    description=(
        "Plataforma de Gestão Administrativa das "
        "Superintendências Federais de Agricultura"
    ),
    version="0.7.0",
)

app.include_router(companies_router)
app.include_router(people_router)
app.include_router(contracts_router)
app.include_router(contract_assignments_router)
app.include_router(competences_router)
app.include_router(competence_steps_router)


@app.get(
    "/",
    tags=["Sistema"],
    summary="Verificar situação do sistema",
)
def root() -> dict[str, str]:
    return {
        "sistema": "PEC-SFA",
        "versao": "0.7.0",
        "status": "online",
    }