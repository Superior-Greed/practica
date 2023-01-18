from fastapi import FastAPI
from routes.routers import user

app = FastAPI()
app.include_router(user)
