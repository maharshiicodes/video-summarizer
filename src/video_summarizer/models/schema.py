from pydantic import BaseModel

class IngestionRequest(BaseModel):
    url : str 

class ChatRequest(BaseModel):
    video_id : str
    question : str