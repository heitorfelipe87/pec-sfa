from app.api.companies import router as companies_router
from app.api.competences import router as competences_router
from app.api.competence_steps import router as competence_steps_router
from app.api.contract_assignments import (
    router as contract_assignments_router,
)
from app.api.contracts import router as contracts_router
from app.api.people import router as people_router

__all__ = [
    "companies_router",
    "competences_router",
    "competence_steps_router",
    "contract_assignments_router",
    "contracts_router",
    "people_router",
]