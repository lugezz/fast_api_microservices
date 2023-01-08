import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-14549.c232.us-east-1-2.ec2.cloud.redislabs.com",
    port=14549,
    password=os.environ.get('REDIS_DB_PASSWORD'),
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quanity: int

    class Meta:
        database = redis


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/products")
def all():
    return Product.all_pks()
