from fastapi import FastAPI, Request, status
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import category, problem, request
from utils.auth_utils import get_authorization

app = FastAPI()

app.include_router(request.router)
app.include_router(problem.router)
app.include_router(category.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def process_request_headers(request: Request, call_next):
    auth = str(get_authorization(request))
    method = str(request.method)
    url = str(request.url)

    if 'chamado' in url or 'problema' in url or 'categoria' in url:
        if method == 'DELETE':
            if auth != 'admin':
                return response_unauthorized
        if method == 'PUT':
            if auth not in ['admin', 'manager']:
                return response_unauthorized

    if method == 'GET' or method == 'POST':
        if 'chamado' in url:
            if auth not in ['admin', 'manager', 'basic', 'public']:
                return response_unauthorized
        elif 'problema' in url or 'categoria' in url:
            if auth not in ['admin', 'manager', 'basic', 'public']:
                return response_unauthorized

    return await call_next(request)


app.include_router(problem.router)
app.include_router(category.router)


@app.get("/")
def root():
    return {"APP": "Detalhador de chamados is running"}


response_unauthorized = JSONResponse({
    "message": "Acesso negado",
    "error": True,
    "data": None,

}, status.HTTP_401_UNAUTHORIZED)
