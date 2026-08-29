from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from video_summarizer.services.ingestion import embedding_model

def query_video(video_id : int,question : str) -> str:
    vector_store = Chroma(
            persist_directory=f"chroma_db/{video_id}",
            embedding_function=embedding_model
        )
    retriever = vector_store.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            "k" : 3,
            "fetch_k" : 10,
            "lambda_mult" : 0.5
        }
    )
    llm = ChatMistralAI(model = "mistral-small-2506")
    
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
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt = prompt.invoke ({
        "context" : context,
        "question" : question
    })
    response = llm.invoke(final_prompt)
    return response.content