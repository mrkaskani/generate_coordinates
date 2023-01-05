from coordinate.noominatim import RandomCoordinate

from fastapi import FastAPI
from pydantic import BaseModel

import uvicorn

app = FastAPI()


class Coordinate(BaseModel):
    location: str
    quantity: int


@app.get('/')
def coordinate(item: Coordinate):
    random = RandomCoordinate(location=item.location, quantity=item.quantity)
    return {"data": random.generate_random_coordinate()}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
