import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import category, problem

app = FastAPI()

app.include_router(problem.router)
app.include_router(category.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"APP": "Detalhador de chamados is running"}
