import os
import openai
import re
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    openai_api_key: str

# Settings 클래스 인스턴스 생성
settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
openai.api_key = settings.openai_api_key

class UrlRequest(BaseModel):
    urlink: str # 사용자가 youtube link입력함.

@app.post("/load") # 반환타입 적기
def get_youtube_text(req: UrlRequest) -> str:
    
    # https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
    url_parts = re.split(r'(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)', req)
    url_value = url_parts[2].split(r'[^0-9a-z_\-]', 1)[0] if url_parts[2] is not None else url_parts[0]
    
    srt = YouTubeTranscriptApi.get_transcript(url_value, languages=['ko'])
    
    text = ''
    # 정규 표현식 패턴으로 종결어미를 찾아 문장 끝에 '.' 추가
    pattern = re.compile(r'(니다|세요|고요|구요|데요|까요|에요|어요|내요|되요|든요|아요|해요|게요|네요|뭡니까)(?=\s|$)')
    
    for i in srt:
        # 정규 표현식을 사용하여 종결어미에 '.' 추가
        modified_text = pattern.sub(r'\1.', i['text'])
        text += modified_text + ' '
    return text

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response = await openai.ChatCompletion.acreate(
        model = "gpt-4",
        message = [
            {"role": "system", "content": "your teacher"},
            {"role": "user", "content": req.message},
        ]
    )
    return ChatRequest(message=response.choices[0].message.content)

# 1. youtube text에 대한 질문 생성
    # 키워드추출로 질문생성할껀가..... 이게 좀 많이 어렵네.. 
# 2. 질문에 대한 답변
    # 웹 서치 vector DB 붙여서 만들기 ----> 관련내용 계속 공부중.....
# 3. 답변에서 또 질문
# 4. 답변 4~5턴 종료 후

# ------------------------------ 추후에 해볼 것
# 비슷한 주제의 동영상 추천받기
# 영상시청 후 ---> 영상 내용 summary. 
# 해당 영상에 대한 질문 답변
# gd

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
