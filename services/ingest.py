from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from main import embedding_model


load_dotenv()

async def ingest_video(url : str):
    loader = YoutubeLoader(
        url,
        add_video_info=false
    )

    data = docs.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    chunks = splitter.split_documents(data)

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = Chroma.from_documents(
        documents = chunks,
        embedding = embedding_model,
        persist_directory = 'chroma_db'
    )