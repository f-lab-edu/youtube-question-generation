import re

import openai
import yt_dlp as yt
from fastapi import FastAPI
from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

import database
from emb import document_split
from model import transcribe_file

app = FastAPI()
database.target_metadata.create_all(bind=database.engine)

AUDIO_FOLDER = "./audio"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    openai_api_key: str


# Settings 클래스 인스턴스 생성
settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
openai.api_key = settings.openai_api_key


class UrlRequest(BaseModel):
    # 사용자가 youtube link 입력함.
    urlink: str


class QuesRequest(BaseModel):
    # 질의를 합니다.
    query: str


@app.post("/youtube_key")
def get_youtube_key(req: UrlRequest) -> str:
    # https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
    url_parts = re.split(r"(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)", req.urlink)
    url_value = url_parts[2].split(r"[^0-9a-z_\-]", 1)[0] if url_parts[2] is not None else url_parts[0]
    return url_value


ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": f"{AUDIO_FOLDER}/%(id)s.%(ext)s",
}


@app.post("/audioload")
def get_youtube_audio(req: UrlRequest):
    # audio 파일이 생성되는데 return type 어떻게 해야할지 모르겠음.
    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download([req])


def audio_to_text(req: UrlRequest, db: database.db_dependency) -> Chroma:
    youtube_urlkey = get_youtube_key(req=req)
    audio_filename = f"./{youtube_urlkey}.webm"
    transcription = transcribe_file(audio_filename)
    db_content = database.User(transcription)
    db.add(db_content)
    db.commit()
    texts = [Document(page_content=transcription)]
    db_content = document_split(texts)
    return db_content


def make_qa_chain(req: UrlRequest, db: database.db_dependency) -> BaseRetrievalQA:
    vector_db = audio_to_text(req, db)
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key="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",
    )
    return RetrievalQA.from_chain_type(
        llm,
        retriever=vector_db.as_retriever(search_type="mmr", search_kwargs={"fetch_k": 3}),
        return_source_documents=True,
    )


@app.post("/chat")
async def ask_question(req: UrlRequest, q: QuesRequest, db: database.db_dependency) -> None:
    qa_chain = make_qa_chain(req, db)
    result = qa_chain({"query": q})
    print(f"Q: {result['query'].strip()}")
    print(f"A: {result['result'].strip()}\n")
    print("\n")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
