FROM python:3

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY main.py .
COPY fetch_posts.py .
COPY util.py .
COPY fetch_media.py .
COPY requirements.txt .


RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]