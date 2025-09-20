from fastapi import FastAPI, HTTPException

from template_service.api import router

app = FastAPI(
    title="Universal Code-Template Generator",
    version="1.0.0",
    docs_url="/",
)
app.include_router(router)