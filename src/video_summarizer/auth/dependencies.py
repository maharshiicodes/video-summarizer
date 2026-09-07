from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from video_summarizer.auth.jwt import decode_access_token
from video_summarizer.db.database import get_db
from video_summarizer.db.models import User

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="not authenticated")

    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="user not found")

    return user