from fastapi import FastAPI
from uuid import UUID, uuid4
from typing import List, Union, Optional, Dict, Any
from pydantic import BaseModel, Field
import uvicorn

# FastAPI 객체 생성
app = FastAPI()

# "/"로 접근하면 return을 보여줌
@app.get("/")
def read_root():
    return {"Hello": "World"}

class Content(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    title : str
    txt : List[str]

class Youtube_Info(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    name : str
    products : List[Content] = Field(default_factory=list)
    creadted_at : datetime = Field(default_factory=datetime.now)
    updated_at : datetime = Field(default_factory=datetime.now)

class MessageResponse(BaseModel):
    message: str
    
youtube_texts = [] #############################################
@app.get()("/info", description="한 youtube의 텍스트들을 가져옵니다.")
async def get_youtube_texts() -> List[Content]:
    # youtube에 있는 크롤링해서 text 추출 code 삽입
    return youtube_texts

@app.get("/info/{youtube_id}", description="youtub 정보를 가져옵니다.")
async def get_youtube(youtube_id: UUID) -> Union[Youtube_Info, MessageResponse]:
    youtube_text = get_youtube_texts() #### 코드 완성 안함.
    if not youtube_text:
        return MessageResponse(message = "추출할 텍스트가 없습니다.")
    return youtube_text

# youtube text받아옴---> text를 기반으로 질문도 생성해야하고, 질문을 qa에 넣으면 답변 생성
@app.post("/info", description="youtube text를 받아와서 질문 생성 및 답변 생성")
async def make_question_answer(texts: List[get_youtube_texts]): #model, # config
    # 1. youtube 텍스트 가져오기
    # 2. 모델에 text넣고 질문 생성
    # 3. 정답확인 (result)
    return