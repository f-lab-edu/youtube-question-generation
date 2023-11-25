FROM python:3.9
COPY . /var/app
WORKDIR /var/app
RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]
