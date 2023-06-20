from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth_router, user_router, jobs_router, response_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(jobs_router)
app.include_router(response_router)

@app.get("/")
def hello():
    return {"message": "Hello, world!"}

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)