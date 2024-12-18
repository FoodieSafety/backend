from fastapi import FastAPI
from middlewares.logging_middleware import log_requests
from .services.user_service import router as user_router
from .services.auth import router as auth_router

# Create a FastAPI instance
app = FastAPI()

# Add middleware
app.middleware("http")(log_requests)

# Include Routers
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def index() -> dict:
    return {"message": "Welcome to Foodie-Safety!"}