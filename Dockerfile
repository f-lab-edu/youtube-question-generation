FROM python:3.11
# dockerhub에서 다운로드 받은 이미지 이름:태그
# 이미지 빌드에 사용할 베이스 이미지를 지정
# 베이스 이미지는 이미 만들어진 이미지
# 보통 처음부터 만들지 않고, 이미 공개된 이미지를 기반으로 새로운 설정을 추가

COPY . /app
# 현재 폴더에 있는 모든 것들을 컨테이너 내부 /app 위치로 옮겨 오겠다. (copy하겠다)
# copy "로컬 디렉토리 (파일)" "컨테이너 내 디렉토리(파일)"
# 컨테이너는 자체적인 파일 시스템과 디렉토리를 가짐
# COPY명령어는 Dockerfile이 존재하는 경로 기준 로컬 디렉토리를 컨테이너 내부의 (자체 파일 시스템을 가진) 디렉토리로 복사
# 해당 코드는 프로젝트 최상위에 존재하는 모든 파일을 컨테이너 내부 /app 디렉토리로 복사
# 파일을 컨테이너에서 사용하려면 COPY명령어로 반드시 복사해야 함
WORKDIR /app
# 컨테이너 내의 디렉토리
# dockerfile의 run, cmd, entrypoint등의 명령어를 실행한 컨테이너 경로 지정
# 이 라인 뒤에 등장하는 run, cmd는 컨테이너 내부의 /app에서 실행
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
# 컨테이너 내의 환경변수를 의미
# 파이썬 애플리케이션의 경우 통상 위 두 값을 지정

# RUN pip install pip==23.0.1 && \
#     pip install poetry==1.2.1 && \
#     poetry export -o requirements.txt && \
#     pip install -r requirements.txt 
# RUN "실행할 리눅스 명령어" 컨테이너 내에서 리눅스 명령어를 실행.
# 한 번에 실행할 명령어가 여러 개인 경우 && \로 이어줌
# 이 전 라인에서 COPY와 WORKDIR이 실행되었기 때문에 컨테이너 내에 requirements.txt이 존재하고,
# 이를 pip install -r 명령어로 실행시킬 수 있음

CMD ["python", "main.py"]
# CMD ["실행할 명령어", "인자", ...]
# docker run으로 이 이미지를 기반으로 컨테이너를 만들 때, 실행할 명령어
# 이 이미지는 실행되는 즉시 python main.py를 실행하여 CMD는 띄어쓰기를 사용하지 않음.

###### run이랑 cmd차이는 무엇일까?!

# 정리
# 그 외에 Dockerfile에서 사용하는 것
# expose : 컨테이너 외부에 노출할 포트 지정
# entrypoint : 이미지를 컨테이너로 띄울 때 항상 실행하는 커멘드 (cmd랑 유사)