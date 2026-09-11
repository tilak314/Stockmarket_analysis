from fastapi import FastAPI

from app.api.stock_routes import router as stock_router
from app.db.init_db import init_db

init_db()


app = FastAPI(
    title="Personal Stock Analysis Agent",
    version="0.1.0"
)


app.include_router(stock_router)


@app.get("/")
def root():
    return {
        "message": "Stock Agent is running"
    }