# main.py

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.results_routes import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
