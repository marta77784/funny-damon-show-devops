FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY youtube_stats.py .

CMD ["python3", "youtube_stats.py"]
