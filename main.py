from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import ChatMistralAI
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

data = YoutubeLoader.from_youtube_url(
    "https://www.youtube.com/watch?v=J7j5tCB_y4w",
    add_video_info = False
)

docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 150
)

chunks = splitter.split_documents(docs)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma.from_documents(
    documents = chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
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


print("rag system created")

print("press 0 to exit")

while True:
    query = input("You : ")
    if query == "0":
        break
    docs = retriever.invoke(query)
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )
    final_prompt = prompt.invoke ({
        "context" : context,
        "question" : query
    })
    response = llm.invoke(final_prompt)

    print(f"\n AI : {response.content}")