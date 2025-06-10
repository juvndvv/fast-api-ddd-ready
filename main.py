import os
from fastapi import FastAPI

from app.Contexts.Shared.Infrastructure.Bootstrap.ApplicationBootstrapper import ApplicationBootstrapper

env_file = os.environ.get("YUREST_ENV_FILE", ".env")

def create_app() -> FastAPI:
    bootstrapper = ApplicationBootstrapper()
    return bootstrapper.app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        lifespan="on"
    ) 
