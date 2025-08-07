import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List

class Fruit(BaseModel):
    name: str

class Fruits(BaseModel):
    fruits: List[Fruit]

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

memory = {"fruits": []}

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/fruits", response_model=Fruits)
def get_fruits():
    return Fruits(fruits=memory["fruits"])

@app.post("/fruits", response_model=Fruit)
def create_fruit(fruit: Fruit):
    memory["fruits"].append(fruit)
    return fruit

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)