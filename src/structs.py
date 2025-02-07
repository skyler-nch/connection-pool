from pydantic import BaseModel

class MongoRequest(BaseModel):
    db: str
    collection: str
    operation: str
    data: dict