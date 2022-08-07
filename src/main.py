import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import category, problem

app = FastAPI()

app.include_router(problem.router)
app.include_router(category.router)

APP_PORT = os.environ.get('APP_PORT', '5000')

origins = [
    f"http://0.0.0.0:{APP_PORT}",
    f"http://localhost:{APP_PORT}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"APP": "Detalhador de chamados is running"}
