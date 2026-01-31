FROM python:3

WORKDIR /app

COPY main.py .
COPY fetch_posts.py .
COPY util.py .
COPY requirements.txt .


RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]