from fastapi import FastAPI
from routers import auth_router, user_router, job_router
import uvicorn

app = FastAPI(swagger_ui_parameters={"persistAuthorization": True})
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(job_router)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)
