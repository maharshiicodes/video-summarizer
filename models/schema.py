from pydantic import BaseModel

class IngestionRequest(BaseModel):
    url : str 

class IngestionResponse(BaseModel):
    