from fastapi import APIRouter,HTTPException,Depends
from video_summarizer.models.schema import ChatRequest
from video_summarizer.db.database import get_db
from sqlalchemy.orm import Session
from video_summarizer.services.rag import query_video
from video_summarizer.db.models import Video
router = APIRouter()

@router.post("/chat")
def chat(request : ChatRequest,db : Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == request.video_id).first()
    if not video:
        raise HTTPException(status_code = 404 , detail = "video not found - ingest it first")

    answer = query_video(request.video_id,request.question)
    return {"answer" : answer}
    