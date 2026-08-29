from video_summarizer.db.database import engine, Base
from video_summarizer.db import models

Base.metadata.create_all(bind=engine)
print("tables created")