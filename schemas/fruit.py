from typing import List

from pydantic import BaseModel


class Fruit(BaseModel):
    name: str


class Fruits(BaseModel):
    fruits: List[Fruit]
