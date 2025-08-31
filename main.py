from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings 
from db.database import create_tables
from routers.load_data import load_data_router

create_tables()  # Create tables at startup if they don't exist


app = FastAPI(
    title="WatchHive API",
    description="API for WatchHive, a colaborative platform to share thoughts and reviews about movies and series.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware, # Enable CORS for frontend development
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(load_data_router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)