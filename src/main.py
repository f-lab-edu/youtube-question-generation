import os
import openai
import re
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

class Settings(BaseSettings):
    openai_api_key: str

# .env 파일에서 환경 변수 로드
load_dotenv()
# Settings 클래스 인스턴스 생성
settings = Settings()
openai.api_key = settings.openai_api_key

class UrlRequest(BaseModel):
    urlink: str # 사용자가 youtube link입력함.

@app.post("/load")
def get_youtube_text(req: UrlRequest):
    
    reg_exp = re.compile(r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*')
    match = reg_exp.match(req)
    url_value = match.group(7) if match and len(match.group(7)) == 11 else False
    
    srt = YouTubeTranscriptApi.get_transcript(url_value, languages=['ko'])
    
    text = ''
    lst = ['니다', '세요', '고요', '구요', '데요', '까요', '에요', '어요', '내요', '되요', '든요', '아요', '해요', '게요', '네요', '뭡니까']

    for i in srt:
        words = i['text'].split(' ')
        sen = ' '.join([word + '.' if word.endswith(j) else word for word in words for j in lst])
        text += sen + ' '
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
    return {"message": response.choices[0].message.content}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
