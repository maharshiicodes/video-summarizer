from celery.exceptions import MaxRetriesExceededError
from video_summarizer.celery_app import celery_app
from video_summarizer.db.database import SessionLocal
from video_summarizer.services.ingestion import ingest_video
from video_summarizer.db.models import Video,VideoStatus,UserVideo

@celery_app.task(bind = True , max_retries = 3,default_retry_delay = 10)
def run_ingestion(self,url:str ,video_id : str , user_id : str):
    db = SessionLocal()
    try:
        ingest_video(url,video_id)

        video = db.query(Video).filter(Video.id == video_id).first()
        video.status = VideoStatus.ready
        db.commit()

    except Exception as e:
        try:
            raise self.retry(exc = e)
        except MaxRetriesExceededError:
            video = db.query(Video).filter(Video.id == video_id).first()
            if video:
                video.status = VideoStatus.failed
                db.commit()
            print(f"ingestion failed for video_id{video_id}")
    finally:
        db.close()