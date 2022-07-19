from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"APP": "Detalhador de chamados is running"}
