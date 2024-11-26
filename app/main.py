from fastapi import FastAPI
from app.routes import auth, users
from app.db import lifespan

app = FastAPI(title="App", version="1.0.0", lifespan=lifespan)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
