FROM python:3.11
COPY . /src
WORKDIR /src
RUN pip install fastapi uvicorn
ENV PYTHONPATH=/src
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "src.main:app", "--host", "127.0.0.1", "--post", "8001"]