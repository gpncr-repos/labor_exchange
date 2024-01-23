import logging

import uvicorn
from fastapi import FastAPI

from src.routers import auth_router, job_router, user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(job_router)

# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - PID:%(process)d - threadName:%(thread)d - %(message)s"
# )


@app.get("/")
def hello():
    return {"message": "Hello, world!"}


# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8080, reload=True)
