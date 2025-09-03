
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.fruit import fruit_router

app = FastAPI()

origins = [
    "http://localhost:5173",
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
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
