from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from video_summarizer.router import ingest,chat ,auth


app = FastAPI()
app.add_middleware(
    CORSMiddleware(
        allow_origins=["http://localhost:3000"],
        allow_credentials = True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
)
app.include_router(chat.router)
app.include_router(ingest.router)
app.include_router(chat.router)