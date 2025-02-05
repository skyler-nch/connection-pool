import os
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

from pymongo import MongoClient
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

from src.mongo_driver import caller

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR,'.env'))

app = FastAPI()

origins = [
    
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
async def mongo(db:str=Form(),collection:str=Form(),operation:str=Form(),data:str=Form()):
    response = caller(MONGOCLIENT,db,collection,operation,json.loads(data))    
    return response

@app.get("/")
async def root():
    return {"message": "Hello World","detail":"connection-pool"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)