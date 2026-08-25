from langchain_community.document_loaders import YoutubeLoader
data = YoutubeLoader.from_youtube_url(
    "https://www.youtube.com/watch?v=J7j5tCB_y4w",
    add_video_info = False
)

docs = data.load()
print(docs[0].page_content)