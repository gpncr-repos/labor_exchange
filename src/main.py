from fastapi import FastAPI
from api import router as api_router
import uvicorn


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router=api_router)

    return app


if __name__ == '__main__':
    uvicorn.run("main:create_app", port=8000, reload=True)
