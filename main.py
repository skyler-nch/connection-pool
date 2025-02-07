import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

from src.mongo_driver import caller
from src.structs import MongoRequest

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR,'.env'))

app = FastAPI()

origins = [
    "http://172.18.0.1:5002",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def connect_to_async_mongo():
    client = AsyncMongoClient(os.getenv("MONGO_CONN_STRING"))
    client = await AsyncMongoClient().aconnect()
    return client

def connect_to_mongo():
    client = MongoClient(os.getenv("MONGO_CONN_STRING"))
    return client

MONGOCLIENT = connect_to_mongo()

@app.post("/mongo")
async def mongo(payload:MongoRequest):
    print(payload)
    response = caller(MONGOCLIENT,**payload.model_dump())    
    return response

@app.get("/")
async def root():
    return {"message": "Hello World","detail":"connection-pool"}
