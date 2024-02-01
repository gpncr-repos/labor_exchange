from fastapi import FastAPI
from api.routers import auth_router, user_router, responses_router, job_router
import uvicorn

app = FastAPI(title="Labor_Exchange")
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(responses_router)
app.include_router(job_router)

@app.get("/")
def hello():
    return {"message": "Hello, world!"}


if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)