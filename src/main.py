from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import category, problem

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problem.router)
app.include_router(category.router)


@app.get("/")
def root():
    return {"APP": "Detalhador de chamados is running"}
