from fastapi import FastAPI
from app.routes import items

app = FastAPI(title="FastAPI DevSecOps Demo")

app.include_router(items.router, prefix="/items")


@app.get("/")
async def root():
    return {"message": "FastAPI DevSecOps demo - healthy"}
