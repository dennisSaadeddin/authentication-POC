# Import required FastAPI components
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

# Import application components
from app.api.auth import router as auth_router
from app.db.base import Base
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown event (optional)
    # Add any cleanup logic here

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Authentication API",
    description="A lightweight authentication API with signup and login endpoints",
    version="1.0.0",
    docs_url="/docs",  # URL for Swagger UI documentation
    redoc_url="/redoc",  # URL for ReDoc documentation
    lifespan=lifespan
)

# Configure CORS (Cross-Origin Resource Sharing)
# In production, replace "*" with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,  # Allows cookies in CORS requests
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all HTTP headers
)

# Include the authentication router with prefix and tags
# This will prepend "/api" to all auth routes
app.include_router(auth_router, prefix="/api", tags=["authentication"])

# Root endpoint for API health check
@app.get("/")
async def root():
    """
    Root endpoint to verify API is running.
    Returns a simple message directing to documentation.
    """
    return {"message": "Authentication API is running. Visit /docs for API documentation."}

# Run the application using uvicorn if script is run directly
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Binds to all network interfaces
        port=8000,       # Port number
        reload=True      # Enable auto-reload during development
    ) 