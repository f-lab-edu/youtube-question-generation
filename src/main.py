import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")

class UrlRequest(BaseModel):
    urlink: str # 사용자가 youtube link입력함.

@app.post("/load")
def get_youtube_text(req: UrlRequest):
    url_value = req.urlink.split('v=')[-1]
    srt = YouTubeTranscriptApi.get_transcript(url_value, languages=['ko'])
    text = ''
    for i in srt:
        words = i['text'].split(' ')
        lst = ['니다', '세요', '고요', '구요', '데요', '까요', '에요', '어요', '내요','되요', '든요', '아요', '해요', '게요', '네요', '뭡니까']
        
        # 문장부호 붙이기
        sen = ''
        for word in words:
            for j in lst:
                if j == word[-len(j):]:
                    word += '.'
            sen += word + ' '
        text += sen
    return text

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    response = openai.ChatCompletion.create(
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