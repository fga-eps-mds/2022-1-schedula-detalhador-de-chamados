from fastapi import FastAPI
from routers import chamado

app = FastAPI()

app.include_router(chamado.router)

@app.get("/")
def root():
    return {"APP": "Detalhador de chamados is running"}
