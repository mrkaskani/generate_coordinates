from coordinate.noominatim import RandomCoordinate

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Coordinate(BaseModel):
    location: str
    quantity: int


@app.get('/')
def coordinate(item: Coordinate):
    random = RandomCoordinate(location=item.location, quantity=item.quantity)
    return {"data": random.generate_random_coordinate()}
