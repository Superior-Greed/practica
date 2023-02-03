from fastapi import FastAPI
from routes.routers import router
from config.db import engine
from models import fences,user

fences.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
