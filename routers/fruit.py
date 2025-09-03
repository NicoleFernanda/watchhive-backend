from fastapi import APIRouter
from schemas.fruit import Fruit, Fruits

fruit_router = APIRouter(prefix="/fruits")

memory = {"fruits": []}


@fruit_router.get("/", response_model=Fruits)
def get_fruits():
    return Fruits(fruits=memory["fruits"])


@fruit_router.post("/", response_model=Fruit)
def create_fruit(fruit: Fruit):
    memory["fruits"].append(fruit)
    return fruit