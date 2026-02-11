from backend.Api_endpoint import router as query_router
from fastapi import FastAPI


app = FastAPI(
    title="Multi-Agent-System",
    version="1.0.0",
    description="Multi-agent backend for document ingestion and intelligent querying"
)


app.include_router(query_router)


