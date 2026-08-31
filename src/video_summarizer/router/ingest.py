from fastapi import APIRouter,HTTPException
from video_summarizer.models.schema import IngestionRequest
from video_summarizer.db.database import get_db
from video_summarizer.db.models import Video,VideoStatus
from video_summarizer.services.ingestion import ingest_video
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()

@router.post('/ingest')
def ingest(request : IngestionRequest,db : Session = Depends(get_db)):
    try:
        video_id = ingest_video(request.url)
    except Exception as e:
        raise HTTPException(status_code = 400 , details = str(e))

    existing = db.query(Video).filter(Video.id == video_id).first()
    if not existing:
        video = Video(id = video_id , status = VideoStatus.ready)
        db.add(video)
        db.commit()
    return {"video_id" : video_id , "status" : "ready"}

