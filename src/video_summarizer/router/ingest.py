from fastapi import APIRouter,HTTPException,Depends,BackgroundTasks
from video_summarizer.models.schema import IngestionRequest
from video_summarizer.db.database import get_db,SessionLocal
from video_summarizer.db.models import Video,VideoStatus
from video_summarizer.services.ingestion import ingest_video , extract_video_id
from sqlalchemy.orm import Session
from video_summarizer.auth.dependencies import get_current_user
from video_summarizer.db.models import User , UserVideo
import uuid

router = APIRouter()

def run_ingestion(url:str ,video_id : str , user_id : str):
    db = SessionLocal()
    try:
        ingest_video(url,video_id)

        video = db.query(Video).filter(Video.id == video_id).first()
        video.title = title
        video.status = VideoStatus.ready
        db.commit()

    except Exception as e:
        video = db.query(Video).filter(Video.id == video_id).first()
        if video:
            video.status = VideoStatus.failed
            db.commit()
        print(e , "ha me madarchod")
        print(f"ingestion failed for video_id{video_id}")
    finally:
        db.close()
    

@router.post('/ingest')
def ingest(request : IngestionRequest,  background_tasks : BackgroundTasks ,db : Session = Depends(get_db) , current_user : User = Depends(get_current_user)):
    try:
        video_id   = extract_video_id(request.url)
    except Exception as e:
        raise HTTPException(status_code = 400 , detail = str(e))

    existing_video = db.query(Video).filter(Video.id == video_id).first()
    if not existing_video:
        video = Video(id = video_id , status = VideoStatus.processing)
        db.add(video)
        db.commit()
        background_tasks.add_task(run_ingestion,request.url,video_id,current_user.id)
    elif existing_video.status == VideoStatus.failed:
        existing_video.status = VideoStatus.processing
        db.commit()
        background_tasks.add_task(run_ingestion,request.url , video_id , current_user.id)

    existing_link = db.query(UserVideo).filter(
        UserVideo.user_id == current_user.id,
        UserVideo.video_id == video_id
    ).first()

    if not existing_link:
        db.add(UserVideo(id = str(uuid.uuid4()) , user_id = current_user.id , video_id = video_id))
        db.commit()
    return {"video_id": video_id, "status": existing_video.status if existing_video else "processing" ,"title" :request. title}

@router.get("/status/{video_id}")
def status(video_id : str , db:Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code = 404 , detail = "video not found")
    return {"video_id" : video.id , "status" : video.status}

