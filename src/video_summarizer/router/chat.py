from fastapi import APIRouter,HTTPException,Depends
from video_summarizer.models.schema import ChatRequest
from video_summarizer.db.database import get_db
from sqlalchemy.orm import Session
from video_summarizer.services.rag import query_video
from video_summarizer.db.models import Video , UserVideo , ChatMessage
from video_summarizer.auth.dependencies import get_current_user
import uuid
router = APIRouter()

@router.post("/chat")
def chat(request : ChatRequest,db : Session = Depends(get_db) , current_user : User = Depends(get_current_user) ):
    video = db.query(Video).filter(Video.id == request.video_id).first()
    if not video:
        raise HTTPException(status_code = 404 , detail = "video not found - ingest it first")
    access = db.query(UserVideo).filter(UserVideo.user_id == current_user.id , UserVideo.video_id == request.video_id).first()
    if not access:
        raise HTTPException(status_code = 404 , detail = "video not found - ingest if first")
    answer = query_video(request.video_id,request.question)
    db.add(ChatMessage(
        id = str(uuid.uuid4()),
        user_id = current_user.id,
        video_id = request.video_id,
        role = "user",
        content = user.question
    ))
    db.add(ChatMessage(
        id = str(uuid.uuid4()),
        user_id = current_user.id,
        video_id = request.video_id,
        role = "assistant",
        content = answer
    ))
    db.commit()
    return {"answer" : answer}

@router.get(f"/chat/{video_id}")
def get_history(video_id : str , db : Session = Depends(get_db) , current_user : User = Depends(get_cuurent_user)):
    access = db.query(UserVideo).filter(UserVideo.user_id == current_user.id , UserVideo.video_id == video_id)
    if not access:
        raise HTTPException(status_code = 404 , detail = "video not found - ingest it first")
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id,
        ChatMessage.video_id == video_id
    ).order_by(ChatMessage.created_at).all()

    return [{"role" : m.role , "content" : m.content , "created_at" : m.created_at} for m in messages]

@router.get("/videos")
def get_videos(db:Session = Depends(get_db) , current_user : User = Depends(get_current_user)):
    