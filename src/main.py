from fastapi import FastAPI
from routers import problem

app = FastAPI()

app.include_router(problem.router)

@app.get("/")
def root():
    return {"APP": "Detalhador de chamados is running"}
