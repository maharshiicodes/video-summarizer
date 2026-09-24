from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from video_summarizer.services.ingestion import embedding_model,PINECONE_INDEX_NAME
from langchain_pinecone import PineconeVectorStore
from sqlalchemy.orm import Session
from video_summarizer.db.models import Chunk
from rank_bm25 import BM25Okapi

def query_video(video_id : str,question : str , db : Session) -> str:
    vector_store = PineconeVectorStore(
            index_name = PINECONE_INDEX_NAME,
            embedding=embedding_model,
            namespace = video_id
        )
    raw_chunks = db.query(Chunk).filter(Chunk.video_id == video_id).all()
    tokenized_corpus = [chunk.content.lower().split(" ") for chunk in raw_chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(question.split(" "))

    scored_chunks = list(zip(scores,raw_chunks))
    scored_chunks.sort(key = lambda x : x[0] , reverse = True)
    bm25_top_chunks = [chunk for score,chunk in scored_chunks[:5]]

    
    retriever = vector_store.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            "k" : 3,
            "fetch_k" : 10,
            "lambda_mult" : 0.5
        }
    )
    llm = ChatGroq(model = "openai/gpt-oss-120b")
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """ 
                You are a binge watcher and a helpful AI assistant who have watched tons and tons of youtube videos and you are an expert to explain youtube videos.
                Use ONLY the provided context to answer the question.
                If the answer is not present in the context,
                say : "I could not find the answer in the document"
    
    
                """
            ),
            (
                "human",
                """ 
               Context : {context}
    
    
    
               question : {question}
               
                """
            )
        ]
    )

    docs = retriever.invoke(question)
    vector_texts = [doc.page_content for doc in docs]
    bm25_texts = [chunk.content for chunk in bm25_top_chunks]
    combined_texts = list(dict.fromkeys(vector_texts + bm25_texts))
    context = "\n\n".join(
       combined_texts
    )

    final_prompt = prompt.invoke ({
        "context" : context,
        "question" : question
    })
    response = llm.invoke(final_prompt)
    return response.content