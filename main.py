# app : 프로젝트 대안 (프로젝트 이름, src등)
# __main__.py는 간단하게 애플리케이션을 실행할 수 있는 Entrypoint역할
    # Entrypoint : 프로그래밍 언어에서 최상위 코드가 실행되는 시작점 또는 프로그램 진입점
# main.py 또는 app.py : FastAPI의 애플리케이션과 Router설정
# model.py는 MLmodel에 대한 클래스와 함수 정의

# 하나의 파일에는 하나의 목적성이 있는 파일을 담는게 좋음 

# app
    # __main__.py
    # main.py
    # model.py

# Poetry : virualenv를 생성해서 격리된 환경에서 빠르게 개발이 가능해짐
    # 기존 파이썬 패키지 관리 도구에서 지원하지 않는 build, Publish가 가능

from fastapi import FastAPI
import uvicorn

# FastAPI 객체 생성
app = FastAPI()


# "/"로 접근하면 return을 보여줌
@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)