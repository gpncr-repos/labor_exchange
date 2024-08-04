import uvicorn
from fastapi import FastAPI

from routers import auth_router, jobs_router, responses_router, user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(jobs_router)
app.include_router(responses_router)


@app.get("/")
def hello():
    """
    Здесь должно быть крутое промо

    """
    return {"message": "Башкирский баш хантер приветствует тебя"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
