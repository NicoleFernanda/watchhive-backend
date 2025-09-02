from fastapi import APIRouter

from schemas.fruit_schemas import Fruit, Fruits

fruits_router = APIRouter(prefix="/fruits")

memory = {'fruits': []}


@fruits_router.get('/', response_model=Fruits)
def get_fruits():
    return Fruits(fruits=memory['fruits'])


@fruits_router.post('/', response_model=Fruit)
def create_fruit(fruit: Fruit):
    memory['fruits'].append(fruit)
    return fruit
