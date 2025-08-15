from fastapi import FastAPI

from app.routers.user_router import user_router

app = FastAPI()

app.include_router(user_router, prefix='/api')

@app.get("/", tags=['Root'])
def read_root():
    return {"message": "Welcome to the FastAPI application!"}



