from fastapi import FastAPI

from routers import category, problem

app = FastAPI()

app.include_router(problem.router)
app.include_router(category.router)


@app.get("/")
def root():
    return {"APP": "Detalhador de chamados is running"}
