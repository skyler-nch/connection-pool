from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from fastapi.exceptions import HTTPException

def _find_one(collection:MongoClient, data:dict):
    response = collection.find_one(data)
    return response

def _insert_one(collection:MongoClient, data:dict):
    id = collection.insert_one(data)
    return {"inserted_id":str(id.inserted_id)}

functions = {"find_one":_find_one,
             "insert_one":_insert_one,
             }

def caller(client:MongoClient, db:str, collection:str,operation:str, data:dict):
    try:
        collection = client[db][collection]
        response = functions[operation](collection, data)
        return response
    except DuplicateKeyError:
        return HTTPException(400,"duplicate key error")
    except KeyError:
        return HTTPException(405,"operation does not exist")
    except:
        return HTTPException(400,"unknown error")

