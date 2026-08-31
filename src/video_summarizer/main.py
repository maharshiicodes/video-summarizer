from fastapi import FastAPI
from video_summarizer.router import ingest,chat


app = FastAPI()
app.include_router(ingest.router)
app.include_router(chat.router)