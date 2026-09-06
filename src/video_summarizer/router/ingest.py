from fastapi import APIRouter,HTTPException,Depends
from video_summarizer.models.schema import IngestionRequest
from video_summarizer.db.database import get_db
from video_summarizer.db.models import Video,VideoStatus
from video_summarizer.services.ingestion import ingest_video
from sqlalchemy.orm import Session
from video_summarizer.auth.dependencies import get_current_user
from video_summarizer.db.models import User , UserVideo
import uuid

router = APIRouter()

@router.post('/ingest')
def ingest(request : IngestionRequest,db : Session = Depends(get_db) , current_user : User = Depends(get_current_user)):
    try:
        video_id = ingest_video(request.url)
    except Exception as e:
        raise HTTPException(status_code = 400 , details = str(e))

    existing_video = db.query(Video).filter(Video.id == video_id).first()
    if not existing:
        video = Video(id = video_id , status = VideoStatus.ready)
        db.add(video)
        db.commit()

    existing_link = db.query(UserVideo).filter(
        UserVideo.user_id == current_user.id,
        UserVideo.video_id == video_id
    ).first()

    if not existing_link:
        db.add(UserVideo(id = str(uuid.uuid4()) , user_id = current_user.id , video_id = video_id))
        db.commit()
    return {"video_id" : video_id , "status" : "ready"}

