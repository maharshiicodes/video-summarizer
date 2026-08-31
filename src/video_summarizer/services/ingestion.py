from dotenv import load_dotenv
import os
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
import re

PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "youtube-rag")

def extract_video_id(url: str) -> str:
    url = "https://www.youtube.com/watch?v=" + url
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if not match:
        raise ValueError("invalid youtube url")
    return match.group(1)


load_dotenv()
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def ingest_video(url : str):
    video_id = extract_video_id(url)
    loader = YoutubeLoader(
        url,
        add_video_info=False
    )

    data = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    chunks = splitter.split_documents(data)

    vector_store = PineconeVectorStore.from_documents(
        documents = chunks,
        embedding = embedding_model,
        index_name = PINECONE_INDEX_NAME,
        namespace = video_id
    )

    return video_id