from fastapi import FastAPI

app = FastAPI(
    title="PEC-SFA",
    description="Painel Executivo de Contratos das Superintendências Federais de Agricultura",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "sistema": "PEC-SFA",
        "versao": "0.1.0",
        "status": "online"
    }
