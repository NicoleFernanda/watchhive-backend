
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.fruit import fruit_router

app = FastAPI(
    root_path="/watchhive/watchhive-backend/v1.0"
)

origins = [
    "http://localhost:5173",
    "https://cb2c9f90-c05a-429e-ad6d-5c4fe716793f.e1-us-east-azure.choreoapps.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fruit_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
