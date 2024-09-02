import os
from pathlib import Path

import uvicorn
from dependency_injector import providers
from fastapi import FastAPI

from config import DBSettings
from dependencies.containers import RepositoriesContainer
from storage.sqlalchemy.client import SqlAlchemyAsync
from web.routers import auth_router, user_router

env_file_name = ".env." + os.environ.get("STAGE", "dev")
env_file_path = Path(__file__).parent.resolve() / env_file_name


def create_app():
    repo_container = RepositoriesContainer()
    settings = DBSettings(_env_file=env_file_path)

    # выбор синхронных / асинхронных реализаций
    repo_container.db.override(
        providers.Factory(
            SqlAlchemyAsync,
            pg_settings=settings,
        ),
    )

    # инициализация приложения
    app = FastAPI()
    app.container = repo_container

    app.include_router(auth_router)
    app.include_router(user_router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
