from video_summarizer.services.ingestion import ingest_video
from video_summarizer.services.rag import query_video

ingest_video("kmy_YNhl0mw")
print(query_video("kmy_YNhl0mw", "what is  react native?"))