from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Enum,Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from video_summarizer.db.database import Base


class VideoStatus(str, enum.Enum):
    processing = "processing"
    ready = "ready"
    failed = "failed"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True)  # = youtube_video_id = Pinecone namespace
    title = Column(String)
    transcript = Column(Text)
    status = Column(Enum(VideoStatus), default=VideoStatus.processing)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserVideo(Base):
    __tablename__ = "user_videos"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Chunk(Base):
    __tablename__ = "video_chunks"
    id = Column(String , primary_key = True , default = lambda : str(uuid.uuid4()))
    video_id = Column(String , ForeignKey("videos.id") , nullable = False)
    chunk_index = Column(Integer,nullable = False )
    content = Column(Text,nullable = False)
    created_at = Column(DateTime(timezone= True) , server_default=func.now())