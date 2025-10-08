from fastapi import FastAPI

from app.api.routes import get_job_id

app = FastAPI(title="Primaa Processing API", version="0.1.0")
app.include_router(get_job_id.router)
